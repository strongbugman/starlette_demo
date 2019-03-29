from starlette.testclient import TestClient


def test_cat(client: TestClient, db, cache):
    data = dict(name="当当", age=2)

    res = client.post("/cats", json=data)
    for k, v in data.items():
        assert res.json()[k] == v

    cat_id = res.json()["id"]
    res = client.get("/cat", params=dict(id=cat_id))
    for k, v in data.items():
        assert res.json()[k] == v

    res = client.get("/cats", params=dict(id=cat_id))
    assert len(res.json()) == 1
    for k, v in data.items():
        assert res.json()[0][k] == v

    res = client.delete("/cat", params=dict(id=cat_id))
    assert res.status_code == 204

    res = client.get("/cat", params=dict(id=cat_id))
    assert res.status_code == 404
