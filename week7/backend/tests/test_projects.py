from sqlalchemy import create_engine, inspect, text

from backend.app.db import ensure_project_relationship_schema


def test_existing_database_gets_project_relationship_column():
    legacy_engine = create_engine("sqlite:///:memory:")
    with legacy_engine.begin() as connection:
        connection.execute(text("CREATE TABLE projects (id INTEGER PRIMARY KEY)"))
        connection.execute(
            text(
                "CREATE TABLE action_items ("
                "id INTEGER PRIMARY KEY, "
                "description TEXT NOT NULL, "
                "completed BOOLEAN NOT NULL"
                ")"
            )
        )

    ensure_project_relationship_schema(legacy_engine)

    columns = {column["name"] for column in inspect(legacy_engine).get_columns("action_items")}
    indexes = {index["name"] for index in inspect(legacy_engine).get_indexes("action_items")}
    assert "project_id" in columns
    assert "ix_action_items_project_id" in indexes


def test_project_lifecycle_and_action_item_relationship(client):
    project_response = client.post(
        "/projects/",
        json={"name": "Launch", "description": "Launch checklist"},
    )
    assert project_response.status_code == 201
    project = project_response.json()
    assert project["action_items"] == []

    item_response = client.post(
        "/action-items/",
        json={"description": "Prepare release notes", "project_id": project["id"]},
    )
    assert item_response.status_code == 201
    item = item_response.json()
    assert item["project_id"] == project["id"]

    detail = client.get(f"/projects/{project['id']}").json()
    assert [entry["id"] for entry in detail["action_items"]] == [item["id"]]
    assert client.get("/action-items/", params={"project_id": project["id"]}).json() == [item]

    patched = client.patch(
        f"/projects/{project['id']}",
        json={"description": "Updated checklist"},
    )
    assert patched.status_code == 200
    assert patched.json()["description"] == "Updated checklist"

    assert client.delete(f"/projects/{project['id']}").status_code == 204
    assert client.get(f"/projects/{project['id']}").status_code == 404
    remaining_item = client.get("/action-items/").json()[0]
    assert remaining_item["project_id"] is None


def test_project_relationship_validation_and_duplicate_names(client):
    payload = {"name": "Roadmap", "description": ""}
    assert client.post("/projects/", json=payload).status_code == 201
    assert client.post("/projects/", json=payload).status_code == 409

    missing_project_item = client.post(
        "/action-items/",
        json={"description": "Orphan", "project_id": 99999},
    )
    assert missing_project_item.status_code == 404


def test_action_item_can_move_between_projects_and_be_unassigned(client):
    first = client.post("/projects/", json={"name": "First"}).json()
    second = client.post("/projects/", json={"name": "Second"}).json()
    item = client.post(
        "/action-items/",
        json={"description": "Move me", "project_id": first["id"]},
    ).json()

    moved = client.patch(
        f"/action-items/{item['id']}",
        json={"project_id": second["id"]},
    )
    assert moved.status_code == 200
    assert moved.json()["project_id"] == second["id"]

    unassigned = client.patch(
        f"/action-items/{item['id']}",
        json={"project_id": None},
    )
    assert unassigned.status_code == 200
    assert unassigned.json()["project_id"] is None
