def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def create_action_item(client, description):
    response = client.post("/action-items/", json={"description": description})
    assert response.status_code == 201, response.text
    return response.json()


def test_list_action_items_filters_by_completion(client):
    open_item = create_action_item(client, "Still open")
    completed_item = create_action_item(client, "Already done")
    response = client.put(f"/action-items/{completed_item['id']}/complete")
    assert response.status_code == 200, response.text

    response = client.get("/action-items/", params={"completed": "false"})
    assert response.status_code == 200, response.text
    assert response.json() == [open_item]

    response = client.get("/action-items/", params={"completed": "true"})
    assert response.status_code == 200, response.text
    assert [item["id"] for item in response.json()] == [completed_item["id"]]

    response = client.get("/action-items/")
    assert response.status_code == 200, response.text
    assert {item["id"] for item in response.json()} == {open_item["id"], completed_item["id"]}


def test_list_action_items_rejects_invalid_filter(client):
    response = client.get("/action-items/", params={"completed": "maybe"})
    assert response.status_code == 422


def test_bulk_complete_marks_all_requested_items_in_request_order(client):
    first = create_action_item(client, "First")
    second = create_action_item(client, "Second")
    untouched = create_action_item(client, "Untouched")

    response = client.post("/action-items/bulk-complete", json={"ids": [second["id"], first["id"]]})
    assert response.status_code == 200, response.text
    assert [item["id"] for item in response.json()] == [second["id"], first["id"]]
    assert all(item["completed"] is True for item in response.json())

    response = client.get("/action-items/", params={"completed": "false"})
    assert response.status_code == 200, response.text
    assert [item["id"] for item in response.json()] == [untouched["id"]]


def test_bulk_complete_rolls_back_when_any_id_is_missing(client):
    first = create_action_item(client, "Must remain open")
    second = create_action_item(client, "Also remains open")

    response = client.post(
        "/action-items/bulk-complete", json={"ids": [first["id"], 999_999, second["id"]]}
    )
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == {
        "message": "One or more action items were not found",
        "missing_ids": [999_999],
    }

    response = client.get("/action-items/", params={"completed": "false"})
    assert response.status_code == 200, response.text
    assert {item["id"] for item in response.json()} == {first["id"], second["id"]}


def test_bulk_complete_validates_id_list(client):
    item = create_action_item(client, "Keep open")

    invalid_payloads = [
        {"ids": []},
        {"ids": [0]},
        {"ids": [-1]},
        {"ids": [item["id"], item["id"]]},
        {"ids": ["not-an-id"]},
    ]
    for payload in invalid_payloads:
        response = client.post("/action-items/bulk-complete", json=payload)
        assert response.status_code == 422, (payload, response.text)

    response = client.get("/action-items/", params={"completed": "false"})
    assert response.status_code == 200, response.text
    assert [action["id"] for action in response.json()] == [item["id"]]
