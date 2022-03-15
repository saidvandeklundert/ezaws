from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
import datetime
from typing import List, Dict
from dateutil.tz import tzutc


class BucketBrief(BaseModel):
    Name: str
    CreationDate: datetime.datetime


class ListBucketsResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    Buckets: List[BucketBrief]
    Owner: Dict[str, str]

    class Config:
        arbitrary_types_allowed = True
