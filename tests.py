import os
import pytest

import motor.motor_asyncio
from pymongo import MongoClient

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

async_db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
async_db = async_db_client.test_local

db_client = MongoClient(os.environ["MONGODB_URL"])
db = db_client.test_local

TEST_AD = dict(
    sdk_version="1.0",
    session_id="001",
    platform='test',
    username='test_username',
    country_code='001'
)


@pytest.fixture(autouse=True)
def run_before_and_after_tests(monkeypatch):
    monkeypatch.setattr('db_utils.db', async_db)

    yield

    for collection_name in db.list_collection_names():
        db[collection_name].drop()

def test_get_ad_increment(monkeypatch):
    response = client.post("/GetAd/", json=TEST_AD)
    assert response.status_code == 200
    el = db["stats"].find_one({"name": f"username-{TEST_AD['username']}"})
    response = client.post("/GetAd/", json=TEST_AD)
    assert response.status_code == 200
    update_el = db["stats"].find_one({"name": f"username-{TEST_AD['username']}"})
    assert el['ad_requests'] + 1 == update_el['ad_requests']


def test_impressions_increment():
    response = client.post("/Impression/", json=TEST_AD)
    assert response.status_code == 200
    el = db["stats"].find_one({"name": f"username-{TEST_AD['username']}"})
    response = client.post("/Impression/", json=TEST_AD)
    assert response.status_code == 200
    update_el = db["stats"].find_one({"name": f"username-{TEST_AD['username']}"})
    assert el['impressions'] + 1 == update_el['impressions']


def test_get_stats():
    client.post("/GetAd/", json=TEST_AD)
    client.post("/Impression/", json=TEST_AD)

    response = client.get("/GetStats/", params={"filter_type": 'username'})

    json_response = response.json()
    assert response.status_code, 200
    assert json_response[0]['ad_requests']
    assert json_response[0]['impressions']
    assert json_response[0]['fill_rate']
