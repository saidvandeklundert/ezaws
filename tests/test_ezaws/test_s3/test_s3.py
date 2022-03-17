from ezaws import S3, S3Bucket, TCBuilder
from ezaws.models.s3 import (
    ListBucketsResponse,
    ObjectMetadata,
    VersioningResponse,
    DeleteObjectResponse,
)
from ezaws import Region
from uuid import uuid4
import pathlib

path = pathlib.Path(__file__).parent.as_posix()
TESTING_FILE = path + "/testing_file.txt"
S3_KEY_NAME = str(uuid4()) + "_testing_key"
S3_KEY_NAME_PUT = str(uuid4()) + "_testing_key"
S3_KEY_NAME_CONTROLLED = str(uuid4()) + "_testing_key"


def test_s3_class():
    """instantiate S3 class and list all buckets"""
    s3 = S3()
    resp = s3.list_buckets()
    assert isinstance(resp, ListBucketsResponse)


def test_s3_bucket():
    """instantiate S3Bucket and check versioning information"""
    bucket = S3Bucket(region=Region.eu_central_1, name="cicdtestingbucket")
    resp = bucket.get_versioning()
    assert isinstance(resp, VersioningResponse)


def test_upload():
    bucket = S3Bucket(region=Region.eu_central_1, name="cicdtestingbucket")

    bucket.upload_file(
        file_name=TESTING_FILE,
        s3_key_name=S3_KEY_NAME,
    )
    resp = bucket.get_object_metadata(s3_file_name=S3_KEY_NAME)
    # only gives a valid return in case the file exists
    assert isinstance(resp, ObjectMetadata)


def test_get_filesize():
    bucket = S3Bucket(region=Region.eu_central_1, name="cicdtestingbucket")
    size_in_mb = bucket.get_file_size(s3_file_name=S3_KEY_NAME)
    size_in_b = bucket.get_file_size(s3_file_name=S3_KEY_NAME, block_size="bytes")
    assert isinstance(size_in_mb, int)
    assert isinstance(size_in_b, int)


def test_delete_key():
    bucket = S3Bucket(region=Region.eu_central_1, name="cicdtestingbucket")
    resp = bucket.delete_object(s3_key_name=S3_KEY_NAME)
    assert isinstance(resp, DeleteObjectResponse)


def test_put():
    bucket = S3Bucket(region=Region.eu_central_1, name="cicdtestingbucket")
    bucket.put_object(file_name=TESTING_FILE, s3_key_name=S3_KEY_NAME_PUT)
    resp = bucket.delete_object(s3_key_name=S3_KEY_NAME_PUT)
    assert isinstance(resp, DeleteObjectResponse)


def test_controlled():
    bucket = S3Bucket(region=Region.eu_central_1, name="cicdtestingbucket")
    bucket.controlled_upload(file_name=TESTING_FILE, s3_key_name=S3_KEY_NAME_CONTROLLED)
    resp = bucket.delete_object(s3_key_name=S3_KEY_NAME_CONTROLLED)
    assert isinstance(resp, DeleteObjectResponse)

    tcbuilder = TCBuilder(use_threads=True, max_concurrency=5)
    bucket.controlled_upload(
        file_name=TESTING_FILE, s3_key_name=S3_KEY_NAME_CONTROLLED, tc=tcbuilder
    )
    resp = bucket.delete_object(s3_key_name=S3_KEY_NAME_CONTROLLED)
    assert isinstance(resp, DeleteObjectResponse)

    tc_dict = {"use_threads": True, "max_concurrency": 5}
    bucket.controlled_upload(
        file_name=TESTING_FILE, s3_key_name=S3_KEY_NAME_CONTROLLED, tc=tc_dict
    )
    resp = bucket.delete_object(s3_key_name=S3_KEY_NAME_CONTROLLED)
    assert isinstance(resp, DeleteObjectResponse)
