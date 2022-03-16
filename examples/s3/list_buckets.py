"""
Display all bucket names
"""
from ezaws import S3

if __name__ == "__main__":
    s3 = S3()
    buckets = s3.list_buckets()
    for bucket_brief in buckets:
        print(bucket_brief.Name)
