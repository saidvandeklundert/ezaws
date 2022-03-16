from ezaws import S3, S3Bucket, Region, TCBuilder


if __name__ == "__main__":
    from pprint import pprint

    s3 = S3()
    resp = s3.list_buckets()
    bucket = S3Bucket(region=Region.eu_central_1, name="s3examplebucketusingezaws")

    bucket.create_bucket()

    resp = bucket.get_versioning()
    pprint(resp.dict())
    resp = bucket.upload_file("example.txt", "some_file")
    import time

    print("UPLOAD DONE")
    time.sleep(2)
    print("upload_file", resp)
    resp = bucket.delete_object(s3_key_name="some_file")
    pprint(resp)

    print("UPLOADING PUT OBJECT")
    resp = bucket.put_object(file_name="example.txt")
    pprint(resp)

    resp = bucket.get_object_metadata(s3_file_name="example.txt")
    print("HEAD OBJECT")
    pprint(resp)
    resp = bucket.get_file_size(s3_file_name="example.txt")
    print("FILESIZE", resp)
    resp = bucket.get_file_size(s3_file_name="example.txt", block_size="bytes")
    print("FILESIZE", resp)

    resp = bucket.delete_object(s3_key_name="example.txt")
    pprint(resp)
    print("CONTROLLED UPLOAD")
    tcbuilder = TCBuilder(use_threads=True, max_concurrency=5)
    resp = bucket.controlled_upload(file_name="example.txt", tc=tcbuilder)
    pprint(resp)
    resp = bucket.delete_object(s3_key_name="example.txt")
    pprint(resp)
    bucket.delete_bucket()
