import boto3
import json
import datetime

# TODO: turn into client
AWS_REGION = "eu-central-1"

client = boto3.client("logs", region_name=AWS_REGION)

response = client.describe_log_groups()

print(json.dumps(response, indent=4))

for each_line in response["logGroups"]:
    print(each_line)

response = client.describe_log_streams(
    logGroupName="/aws/lambda/klundert-lambda-sam-helloworldpython3-6BxLjAQrMYOi"
)
print(response)

response = client.get_log_events(
    logGroupName="/aws/lambda/klundert-lambda-sam-helloworldpython3-6BxLjAQrMYOi",
    logStreamName="2021/12/31/[$LATEST]c525e839ab9f4d218505751ab71e9f3f",
    limit=123,
    startFromHead=True,
)

log_events = response["events"]

for each_event in log_events:
    print(each_event)
