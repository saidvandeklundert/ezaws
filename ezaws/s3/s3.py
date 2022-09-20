import boto3
from boto3.s3.transfer import TransferConfig, S3Transfer
from ezaws.models.s3 import (
    ListBucketsResponse,
    CreateBucketResponse,
    DeleteBucketResponse,
    VersioningResponse,
    ObjectMetadata,
    PutObjectResponse,
    DeleteObjectResponse,
    TCBuilder,
)
from typing import Any, Union, Literal, Optional, Dict
from dataclasses import dataclass


KB = 1024
MB = KB * KB


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

    def get_object_metadata(self, s3_file_name: str) -> ObjectMetadata:
        """
        Display metadata for target file stored in S3
        """
        s3 = boto3.client("s3")
        response = s3.head_object(Bucket=self.name, Key=s3_file_name)
        return ObjectMetadata(**response)

    def get_file_size(
        self, s3_file_name: str, block_size: Literal["bytes", "MB"] = "MB"
    ) -> int:
        """
        List a file from S3
        """
        resp = self.get_object_metadata(s3_file_name=s3_file_name)
        size = resp.ContentLength

        if block_size == "bytes":
            return int(size)
        elif block_size == "MB":
            return int(size / MB)

    def put_object(
        self, file_name: str, s3_key_name: Optional[str] = None
    ) -> PutObjectResponse:
        """Put an object in S3"""
        s3_key_name = s3_key_name if s3_key_name is not None else file_name
        s3 = boto3.client("s3")

        resp = s3.put_object(Body=file_name, Bucket=self.name, Key=s3_key_name)
        return PutObjectResponse(**resp)

    def upload_file(self, file_name: str, s3_key_name: Optional[str] = None) -> Any:
        """Upload a file to S3 using upload_file

        TODO: examine all of the upload_file possible returns.

        add optional argument to satisfy 'ExtraArgs={'Metadata': {'mykey': 'myvalue'}'
         from https://boto3.amazonaws.com/v1/documentation/api/latest/reference/customizations/s3.html#boto3.s3.transfer.S3Transfer.ALLOWED_UPLOAD_ARGS
        """
        s3_key_name = s3_key_name if s3_key_name is not None else file_name
        s3 = boto3.client("s3")

        resp = s3.upload_file(file_name, self.name, s3_key_name)

        return resp

    def controlled_upload(
        self,
        file_name: str,
        s3_key_name: Optional[str] = None,
        tc: Optional[Union[TCBuilder, Dict]] = None,
    ) -> None:

        """
        Upload a file to S3 with more fine-grained control.

        tc is a Union of either of the following:
          - None: in which case the TransferConfig() defaults are used
          - TCBuilder: a model for dev ergonmics that you can use to
           instantiate an instance of TransferConfig()
          - Dict: a dict that is used to instantiate an instance of TransferConfig()

        The TransferConfig description:
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
        s3_key_name = s3_key_name if s3_key_name is not None else file_name

        session = boto3.Session()
        if tc is None:
            tc_config = TransferConfig()  # use default
        elif isinstance(tc, TCBuilder):
            tc_config = TransferConfig(
                **{k: v for (k, v) in tc.dict().items() if v is not None}
            )
        elif isinstance(tc, dict):
            tc_config = TransferConfig(**tc)

        s3_client = session.client("s3")
        transfer_object = S3Transfer(client=s3_client, config=tc_config)
        transfer_object.upload_file(file_name, self.name, s3_key_name)

    def delete_object(
        self, s3_key_name: str, version_id: Optional[str] = None
    ) -> DeleteObjectResponse:
        """Deletes an object from the bucket."""
        s3 = boto3.client("s3")
        del_args = {"Bucket": self.name, "Key": s3_key_name}
        if version_id:
            del_args.update({"VersionID": version_id})

        response = s3.delete_object(**del_args)
        return DeleteObjectResponse(**response)

    def empty(self) -> None:
        raise NotImplementedError

    def set_encryption(self) -> None:
        raise NotImplementedError

    def set_versioning(self) -> None:
        raise NotImplementedError
