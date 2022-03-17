from ezaws import S3Bucket, Region

from pprint import pprint

BUCKET_NAME = "cicdtestingbucket"
if __name__ == "__main__":
    bucket = S3Bucket(region=Region.eu_central_1, name=BUCKET_NAME)

    print("CREATE BUCKET\n\n")
    resp = bucket.create_bucket()
    pprint(resp)
