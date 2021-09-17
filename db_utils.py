import os
import motor.motor_asyncio

from typing import Optional

from models import StatsModel


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.local


async def increment_ad_requests(field_name: str):
    return await db["stats"].update_one({"name": field_name}, {"$inc": {"ad_requests": 1}}, True)


async def increment_impressions(field_name: str):
    return await db["stats"].update_one({"name": field_name}, {"$inc": {"impressions": 1}}, True)


async def get_element_by_filter_value(filter_type: str) -> Optional[StatsModel]:
    obj = await db["stats"].find_one({"name": f"username-{filter_type}"})
    if obj is None:
        obj = await db["stats"].find_one({"name": f"sdk_version-{filter_type}"})
    if obj is not None:
        obj = StatsModel(ad_requests=obj.get('ad_requests', 0), impressions=obj.get('impressions', 0))

    return obj
