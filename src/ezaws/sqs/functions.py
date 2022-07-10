import boto3


from ezaws.models.sqs import (
    GetQueueResponse,
    CreateQueueResponse,
    DeleteQueueResponse,
    ListQueueResponse,
    PurgeQueueResponse,
    SendMessageResponse,
    ReadMessageResponse,
    DeleteMessageResponse,
)


def create_queue(queue_name: str, region: str) -> CreateQueueResponse:
    """ "Create an SQS queue."""
    client = boto3.client("sqs", region_name=region)
    response = client.create_queue(
        QueueName=queue_name,
        Attributes={
            "DelaySeconds": "5",  # default 0, max 900 (15 min)
            "VisibilityTimeout": "29",  # default 30, min 0
        },
    )
    return CreateQueueResponse(**response)


def get_queue_url(queue_name: str) -> GetQueueResponse:
    sqs_client = boto3.client("sqs", region_name="eu-central-1")
    response = sqs_client.get_queue_url(
        QueueName=queue_name,
    )
    return GetQueueResponse(**response)


def delete_queue(queue_name: str, region: str) -> DeleteQueueResponse:
    sqs_client = boto3.client("sqs", region_name=region)
    response = sqs_client.delete_queue(QueueUrl=queue_name)
    return DeleteQueueResponse(**response)


def purge_queue(queueu_url: str, region_name: str) -> PurgeQueueResponse:
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.purge_queue(QueueUrl=queueu_url)
    return PurgeQueueResponse(**response)


def send_message(
    queueu_url: str, region_name: str, message: str
) -> SendMessageResponse:
    sqs_client = boto3.client("sqs", region_name=region_name)

    response = sqs_client.send_message(QueueUrl=queueu_url, MessageBody=message)
    return SendMessageResponse(**response)


def read_message(
    queueu_url: str, region_name: str, nr_of_messages: int = 1
) -> ReadMessageResponse:
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.receive_message(
        QueueUrl=queueu_url,
        MaxNumberOfMessages=nr_of_messages,  # max 10, default 1
        WaitTimeSeconds=0,
    )
    return ReadMessageResponse(**response)


def delete_message(
    queueu_url: str, region_name: str, receipt_handle: str
) -> DeleteMessageResponse:
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.delete_message(
        QueueUrl=queueu_url,
        ReceiptHandle=receipt_handle,
    )

    return DeleteMessageResponse(**response)


def list_queues(region: str, max_results: int = 100) -> ListQueueResponse:
    """Returns a list of URLs inside a ListQueueResponse,
    listing all the queues in a region."""
    sqs_client = boto3.client("sqs", region_name=region)

    response = sqs_client.list_queues(MaxResults=max_results)
    return ListQueueResponse(**response)
