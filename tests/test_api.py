from starlette.testclient import TestClient
from starlette.applications import Starlette
from openapi_spec_validator import validate_v3_spec

from app.extensions import starchart


def test_schema(app: Starlette):
    validate_v3_spec(starchart.schema_generator.get_schema(app.routes))


def test_cat(client: TestClient, db, cache):
    data = dict(name="当当", age=2)

    data = dict(name="丁丁", age=1)
    res = client.post("/cats", json=data)
    for k, v in data.items():
        assert res.json()[k] == v
    cat1_id = res.json()["id"]

    res = client.post("/cats", json=data)
    for k, v in data.items():
        assert res.json()[k] == v
    cat2_id = res.json()["id"]

    res = client.get("/cat", params=dict(id=cat2_id))
    for k, v in data.items():
        assert res.json()[k] == v

    res = client.get("/cats")
    assert len(res.json()) == 2
    for k, v in data.items():
        assert res.json()[0][k] == v

    res = client.delete("/cat", params=dict(id=cat1_id))
    assert res.status_code == 204
    res = client.delete("/cat", params=dict(id=cat2_id))
    assert res.status_code == 204

    res = client.get("/cat", params=dict(id=cat2_id))
    assert res.status_code == 404
