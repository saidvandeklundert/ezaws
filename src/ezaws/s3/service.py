import boto3
from ezaws.models.s3 import ListBucketsResponse


class S3:
    def list_buckets(self) -> ListBucketsResponse:
        """List all buckets using S3 client."""
        s3 = boto3.client(
            "s3",
        )

        response = s3.list_buckets()
        return ListBucketsResponse(**response)


if __name__ == "__main__":
    s3 = S3()
    resp = s3.list_buckets()
