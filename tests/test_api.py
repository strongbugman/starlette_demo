from starlette.testclient import TestClient
from starlette.applications import Starlette
from openapi_spec_validator import validate_v3_spec

from app.extensions import apiman


def test_schema(app: Starlette):
    validate_v3_spec(apiman.specification)


def test_health(client: TestClient):
    res = client.get("/health/")
    assert res.status_code == 200


def test_cat(client: TestClient, db, cache):
    # create
    data = dict(name="丁丁", age=1)
    res = client.post("/cats/", json=data)
    for k, v in data.items():
        assert res.json()[k] == v
    cat1_id = res.json()["id"]

    data = dict(name="当当", age=2)
    res = client.post("/cats/", json=data)
    for k, v in data.items():
        assert res.json()[k] == v
    cat2_id = res.json()["id"]
    # get
    res = client.get("/cat/", params=dict(id=cat2_id))
    for k, v in data.items():
        assert res.json()[k] == v
    # get with wrong id
    res = client.get("/cat/", params=dict(id="abc"))
    assert res.status_code == 400
    # get cat1
    res = client.get("/cats/")
    assert len(res.json()["objects"]) == 2
    assert res.json()["objects"][0]["id"] == cat1_id
    # update
    data["id"] = cat2_id
    data["age"] += 1
    res = client.put("/cat/", json=data)
    for k, v in data.items():
        assert res.json()[k] == v
    cat2_id = res.json()["id"]
    # update with no json data
    res = client.put("/cat/")
    assert res.status_code == 400
    # update with wrong data format
    data["name"] = "*" * 33
    res = client.put("/cat/", json=data)
    assert res.status_code == 400
    # delete
    res = client.delete("/cat/", params=dict(id=cat1_id))
    assert res.status_code == 204
    res = client.delete("/cat/", params=dict(id=cat2_id))
    assert res.status_code == 204

    res = client.get("/cat/", params=dict(id=cat2_id))
    assert res.status_code == 404
