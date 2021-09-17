from enum import Enum

from bson import ObjectId
from pydantic import BaseModel, Field


class FilterType(Enum):
    username = 'username'
    sdk_version = 'sdk_version'


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class StatsModel(BaseModel):
    name: str = Field(...)
    ad_requests: int = Field(...)
    impressions: int = Field(...)

    @property
    def fill_rate(self):
        return self.impressions / self.ad_requests if self.ad_requests else 0

    def to_dict(self):
        return {
            'name': self.name,
            'ad_requests': self.ad_requests,
            'impressions': self.impressions,
            'fill_rate': self.fill_rate
        }


class ADModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    sdk_version: str
    session_id: str
    platform: str
    username: str
    country_code: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "sdk_version": "1.0",
                "session_id": "1",
                "platform": "Example Platform",
                "username": "Example Username",
                "country_code": "101"
            }
        }
