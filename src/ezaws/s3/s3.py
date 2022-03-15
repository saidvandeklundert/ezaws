from ensurepip import version
import boto3
from ezaws.models.s3 import (
    ListBucketsResponse,
    CreateBucketResponse,
    DeleteBucketResponse,
    VersioningResponse,
)
from ezaws.models.regions import Region
from typing import Union
from dataclasses import dataclass
from pydantic import BaseModel


class S3:
    def list_buckets(self) -> ListBucketsResponse:
        """List all buckets using S3 client."""
        s3 = boto3.client(
            "s3",
        )

        response = s3.list_buckets()
        return ListBucketsResponse(**response)


@dataclass
class S3Bucket:
    region: str
    name: str

    def create_bucket(self) -> CreateBucketResponse:
        """Create the bucket for this class."""
        s3_client = boto3.client("s3")
        resp_bucket_creation = s3_client.create_bucket(
            Bucket=self.name,
            CreateBucketConfiguration={"LocationConstraint": self.region},
        )

        return CreateBucketResponse(**resp_bucket_creation)

    def delete_bucket(self) -> DeleteBucketResponse:
        """Delete this bucket"""
        s3_resource = boto3.resource("s3")
        delete_response = s3_resource.Bucket(self.name).delete()
        return DeleteBucketResponse(**delete_response)

    def get_versioning(self) -> VersioningResponse:
        """Return versioning information for this bucket."""
        s3_client = boto3.client("s3")
        versioning_response = s3_client.get_bucket_versioning(Bucket=self.name)

        return VersioningResponse(**versioning_response)

    def upload_file(self):
        raise NotImplementedError

    def upload_large_file(self):
        raise NotImplementedError

    def empty(self):
        raise NotImplementedError

    def set_encryption(self):
        raise NotImplementedError

    def set_versioning(self):
        raise NotImplementedError

    def get_object_metadata(self):
        raise NotImplementedError

    def delete_file(self):
        raise NotImplementedError

    def get_file_size(self):
        raise NotImplementedError


if __name__ == "__main__":
    from pprint import pprint

    s3 = S3()
    resp = s3.list_buckets()
    bucket = S3Bucket(region=Region.eu_central_1, name="createingbucket")
    # bucket.create_bucket()
    # bucket.delete_bucket()
    resp = bucket.get_versioning()
    pprint(resp.dict())
