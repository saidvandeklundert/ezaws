from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
import datetime
from typing import List, Dict, Optional, Literal, Any
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


class CreateBucketResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    Location: str


class DeleteBucketResponse(BaseModel):
    ResponseMetadata: ResponseMetadata


class VersioningResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    Status: Optional[Literal["Enabled", "Suspended"]]
    MFADelete: Optional[Literal["Enabled", "Disabled"]]
    versioning: bool = False

    def __post_init__(self):
        if self.Status == "Enabled":
            self.versioning = True


class ObjectMetadata(BaseModel):
    ResponseMetadata: ResponseMetadata
    AcceptRanges: str
    ContentLength: int
    ContentType: str
    ETag: str
    LastModified: datetime.datetime
    Metadata: Dict[Any, Any]
    SSEKMSKeyId: str
    ServerSideEncryption: str
    VersionId: str
