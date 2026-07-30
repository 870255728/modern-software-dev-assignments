import pytest


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        ("/notes/", {"title": "   ", "content": "content"}),
        ("/notes/", {"title": "title", "content": "\n\t"}),
        ("/action-items/", {"description": " "}),
    ],
)
def test_create_rejects_blank_text(client, path, payload):
    response = client.post(path, json=payload)

    assert response.status_code == 422


@pytest.mark.parametrize("path", ["/notes/", "/action-items/"])
@pytest.mark.parametrize(
    "params",
    [
        {"skip": -1},
        {"limit": 0},
        {"limit": 201},
        {"sort": "not_a_column"},
    ],
)
def test_list_rejects_invalid_query_parameters(client, path, params):
    response = client.get(path, params=params)

    assert response.status_code == 422


@pytest.mark.parametrize("path", ["/notes/99999", "/action-items/99999"])
def test_detail_and_delete_return_not_found(client, path):
    assert client.get(path).status_code == 404
    assert client.delete(path).status_code == 404


def test_get_and_delete_resources(client):
    note = client.post("/notes/", json={"title": " Keep ", "content": " tidy "}).json()
    item = client.post("/action-items/", json={"description": " Ship it "}).json()

    assert note["title"] == "Keep"
    assert item["description"] == "Ship it"
    assert client.get(f"/action-items/{item['id']}").json() == item

    assert client.delete(f"/notes/{note['id']}").status_code == 204
    assert client.delete(f"/action-items/{item['id']}").status_code == 204
    assert client.get(f"/notes/{note['id']}").status_code == 404
    assert client.get(f"/action-items/{item['id']}").status_code == 404
