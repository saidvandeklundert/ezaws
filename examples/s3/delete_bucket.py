from ezaws import S3Bucket, Region
import time
from pprint import pprint

BUCKET_NAME = "s3examplebucketusingezaws"

if __name__ == "__main__":
    bucket = S3Bucket(region=Region.eu_central_1, name=BUCKET_NAME)
    print("DELETE BUCKET\n\n")
    resp = bucket.delete_bucket()
    pprint(resp)
