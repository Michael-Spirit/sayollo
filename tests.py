import os

from pymongo import MongoClient

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
db_client = MongoClient(os.environ["MONGODB_URL"])
db = db_client.local

def test_get_ad_increment():
    ad = dict(
        sdk_version="1.0",
        session_id="001",
        platform='test',
        username='test_username',
        country_code='001'
    )

    response = client.post("/ads/", json=ad)
    assert response.status_code == 200
    el = db["stats"].find_one({"name": f"username-{ad['username']}"})
    response = client.post("/ads/", json=ad)
    assert response.status_code == 200
    update_el = db["stats"].find_one({"name": f"username-{ad['username']}"})
    assert el['ad_requests'] + 1 == update_el['ad_requests']


def test_impressions_increment():
    ad = dict(
        sdk_version="1.0",
        session_id="001",
        platform='test',
        username='test_username',
        country_code='001'
    )

    response = client.post("/impressions/", json=ad)
    assert response.status_code == 200
    el = db["stats"].find_one({"name": f"username-{ad['username']}"})
    response = client.post("/impressions/", json=ad)
    assert response.status_code == 200
    update_el = db["stats"].find_one({"name": f"username-{ad['username']}"})
    assert el['impressions'] + 1 == update_el['impressions']


def test_get_stats():
    response = client.get("/get_stats/", params={"filter_type": 'test_username'})

    json_response = response.json()
    assert response.status_code, 200
    assert json_response['ad_requests']
    assert json_response['impressions']
    assert json_response['fill_rate']
