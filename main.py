import requests

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

from db_utils import get_element_by_filter_value, increment_ad_requests, increment_impressions
from models import ADModel, StatsModel

app = FastAPI()


AD_URL = 'https://6u3td6zfza.execute-api.us-east-2.amazonaws.com/prod/ad/vast'


@app.post("/ads/")
async def get_ad(ad: ADModel):
    await increment_ad_requests(f"username-{ad.username}")
    await increment_ad_requests(f"sdk_version-{ad.sdk_version}")

    response = requests.get(AD_URL)
    return Response(content=response.content)


@app.post("/impressions/")
async def impressions(ad: ADModel):
    await increment_impressions(f"username-{ad.username}")
    await increment_impressions(f"sdk_version-{ad.sdk_version}")

    return Response(status_code=200)


@app.get("/get_stats/", response_description="Username or SDK_Version stats", response_model=StatsModel)
async def get_stats(filter_type: str):
    obj = await get_element_by_filter_value(filter_type)
    if obj is None:
        return Response(status_code=404)

    return JSONResponse(obj.to_dict())
