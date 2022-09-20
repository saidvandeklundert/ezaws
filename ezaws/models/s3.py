from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
import datetime
from typing import List, Dict, Optional, Literal, Any, Iterator


class BucketBrief(BaseModel):
    Name: str
    CreationDate: datetime.datetime


class ListBucketsResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    Buckets: List[BucketBrief]
    Owner: Dict[str, str]

    class Config:
        arbitrary_types_allowed = True

    def __iter__(self) -> Any:
        return iter(self.Buckets)


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

    def __post_init__(self) -> None:
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
    SSEKMSKeyId: Optional[str]
    ServerSideEncryption: Optional[str]
    VersionId: Optional[str]


class PutObjectResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    ETag: Optional[str]
    Expiration: Optional[str]
    ChecksumCRC32: Optional[str]
    ChecksumCRC32C: Optional[str]
    ChecksumSHA1: Optional[str]
    ChecksumSHA256: Optional[str]
    ServerSideEncryption: Optional[Literal["AES256", "aws:kms"]]
    VersionId: Optional[str]
    SSECustomerAlgorithm: Optional[str]
    SSECustomerKeyMD5: Optional[str]
    SSEKMSKeyId: Optional[str]
    SSEKMSEncryptionContext: Optional[str]
    BucketKeyEnabled: Optional[bool]
    RequestCharged: Optional[str]


class DeleteObjectResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    DeleteMarker: Optional[bool]
    VersionId: Optional[str]
    RequestCharged: Optional[str]


class TCBuilder(BaseModel):
    """
    Serves as arg ot the TransferConfig:
      https://boto3.amazonaws.com/v1/documentation/api/latest/_modules/boto3/s3/transfer.html#TransferConfig

    TransferConfig example (default values):

            TransferConfig(
                multipart_threshold=8 * MB,
                max_concurrency=10,
                multipart_chunksize=8 * MB,
                num_download_attempts=5,
                max_io_queue=100,
                io_chunksize=256 * KB,
                use_threads=True,
                max_bandwidth=None,
            )
    """

    multipart_threshold: Optional[int]
    max_concurrency: Optional[int]
    multipart_chunksize: Optional[int]
    use_threads: Optional[bool]
    num_download_attempts: Optional[int]
    max_io_queue: Optional[int]
    io_chunksize: Optional[int]
    max_bandwidth: Optional[int]
