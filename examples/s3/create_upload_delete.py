from ezaws import S3Bucket, Region
import time
from pprint import pprint

BUCKET_NAME = "s3examplebucketusingezaws"
if __name__ == "__main__":
    bucket = S3Bucket(region=Region.eu_central_1, name=BUCKET_NAME)

    print("CREATE BUCKET\n\n")
    resp = bucket.create_bucket()
    pprint(resp)

    print("UPLOAD FILE\n\n")
    resp = bucket.upload_file("example.txt", "some_file")
    pprint(resp)

    time.sleep(2)

    print("GET OBJECT METADATA\n\n")
    resp = bucket.get_object_metadata(s3_file_name="some_file")
    pprint(resp)

    print("DELETE FILE\n\n")
    resp = bucket.delete_object(s3_key_name="some_file")
    pprint(resp)

    print("DELETE BUCKET\n\n")
    resp = bucket.delete_bucket()
    pprint(resp)
