import os
from typing import List

import motor.motor_asyncio

from models import StatsModel, FilterType

client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.local


async def increment_ad_requests(field_name: str):
    return await db["stats"].update_one({"name": field_name}, {"$inc": {"ad_requests": 1}}, True)


async def increment_impressions(field_name: str):
    return await db["stats"].update_one({"name": field_name}, {"$inc": {"impressions": 1}}, True)


async def get_stats_by_filter_type(filter_type: FilterType) -> List[StatsModel]:
    stats = []

    cursor = db["stats"].find({"name": {"$regex": f"^{filter_type.value}"}})
    async for cur in cursor:
        stats.append(
            StatsModel(
                name=cur['name'],
                ad_requests=cur.get('ad_requests', 0),
                impressions=cur.get('impressions', 0)
            )
        )

    return stats
