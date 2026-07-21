import pytest


def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_update_note(client):
    created = client.post("/notes/", json={"title": "Original", "content": "Before"}).json()

    response = client.put(
        f"/notes/{created['id']}",
        json={"title": "Revised", "content": "After"},
    )

    assert response.status_code == 200, response.text
    assert response.json() == {
        "id": created["id"],
        "title": "Revised",
        "content": "After",
    }
    assert client.get(f"/notes/{created['id']}").json()["title"] == "Revised"


def test_delete_note(client):
    created = client.post("/notes/", json={"title": "Disposable", "content": "Delete me"}).json()

    response = client.delete(f"/notes/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/notes/{created['id']}").status_code == 404
    assert client.get("/notes/").json() == []


def test_update_missing_note_returns_404(client):
    response = client.put("/notes/999", json={"title": "Missing", "content": "No note"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


def test_delete_missing_note_returns_404(client):
    response = client.delete("/notes/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Note not found"}


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "content": "Valid content"},
        {"title": "x" * 201, "content": "Valid content"},
        {"title": "Valid title", "content": ""},
        {"title": "Valid title", "content": "x" * 10_001},
    ],
)
def test_create_note_rejects_invalid_payload(client, payload):
    response = client.post("/notes/", json=payload)

    assert response.status_code == 422
    assert client.get("/notes/").json() == []


@pytest.mark.parametrize(
    "payload",
    [
        {"title": "", "content": "Valid content"},
        {"title": "x" * 201, "content": "Valid content"},
        {"title": "Valid title", "content": ""},
        {"title": "Valid title", "content": "x" * 10_001},
    ],
)
def test_update_note_rejects_invalid_payload_without_changes(client, payload):
    created = client.post("/notes/", json={"title": "Original", "content": "Unchanged"}).json()

    response = client.put(f"/notes/{created['id']}", json=payload)

    assert response.status_code == 422
    assert client.get(f"/notes/{created['id']}").json() == created
