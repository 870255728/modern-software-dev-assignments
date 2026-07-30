import pytest


def create_notes(client, titles):
    return [
        client.post(
            "/notes/",
            json={"title": title, "content": f"Content for {title}"},
        ).json()
        for title in titles
    ]


def create_action_items(client, descriptions):
    return [
        client.post("/action-items/", json={"description": description}).json()
        for description in descriptions
    ]


@pytest.mark.parametrize(
    ("sort", "expected"),
    [
        ("title", ["Alpha", "Bravo", "Charlie", "Delta"]),
        ("-title", ["Delta", "Charlie", "Bravo", "Alpha"]),
    ],
)
def test_notes_sort_in_both_directions(client, sort, expected):
    create_notes(client, ["Delta", "Alpha", "Charlie", "Bravo"])

    response = client.get("/notes/", params={"sort": sort})

    assert response.status_code == 200
    assert [note["title"] for note in response.json()] == expected


def test_notes_apply_sort_before_pagination(client):
    create_notes(client, ["Delta", "Alpha", "Charlie", "Bravo"])

    response = client.get(
        "/notes/",
        params={"sort": "title", "skip": 1, "limit": 2},
    )

    assert response.status_code == 200
    assert [note["title"] for note in response.json()] == ["Bravo", "Charlie"]


def test_note_search_composes_with_pagination_and_sorting(client):
    create_notes(client, ["Release C", "Unrelated", "Release A", "Release B"])

    response = client.get(
        "/notes/",
        params={"q": "Release", "sort": "title", "skip": 1, "limit": 1},
    )

    assert response.status_code == 200
    assert [note["title"] for note in response.json()] == ["Release B"]


@pytest.mark.parametrize(
    ("sort", "expected"),
    [
        ("description", ["Alpha", "Bravo", "Charlie", "Delta"]),
        ("-description", ["Delta", "Charlie", "Bravo", "Alpha"]),
    ],
)
def test_action_items_sort_in_both_directions(client, sort, expected):
    create_action_items(client, ["Delta", "Alpha", "Charlie", "Bravo"])

    response = client.get("/action-items/", params={"sort": sort})

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == expected


def test_action_items_apply_filter_and_sort_before_pagination(client):
    items = create_action_items(client, ["Done C", "Open", "Done A", "Done B"])
    for item in (items[0], items[2], items[3]):
        response = client.put(f"/action-items/{item['id']}/complete")
        assert response.status_code == 200

    response = client.get(
        "/action-items/",
        params={
            "completed": True,
            "sort": "description",
            "skip": 1,
            "limit": 1,
        },
    )

    assert response.status_code == 200
    assert [item["description"] for item in response.json()] == ["Done B"]


@pytest.mark.parametrize("path", ["/notes/", "/action-items/"])
def test_limit_zero_returns_an_empty_page(client, path):
    response = client.get(path, params={"limit": 0})

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.parametrize("path", ["/notes/", "/action-items/"])
def test_limit_over_maximum_is_rejected(client, path):
    response = client.get(path, params={"limit": 201})

    assert response.status_code == 422


@pytest.mark.parametrize("path", ["/notes/", "/action-items/"])
def test_unknown_sort_falls_back_to_created_at_descending(client, path):
    if path == "/notes/":
        created = create_notes(client, ["First", "Second", "Third"])
    else:
        created = create_action_items(client, ["First", "Second", "Third"])

    response = client.get(path, params={"sort": "unknown"})

    assert response.status_code == 200
    assert [entry["id"] for entry in response.json()] == [
        entry["id"] for entry in reversed(created)
    ]
