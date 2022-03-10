'''
def create_queue(queue_name: str, region_name: str) -> CreateQueueResponse:
    client = boto3.client("sqs", region_name=region_name)
    response = client.create_queue(
        QueueName=queue_name,
        Attributes={
            "DelaySeconds": "5",  # default 0, max 900 (15 min)
            "VisibilityTimeout": "29",  # default 30, min 0
        },
    )
    return CreateQueueResponse(**response)

@dataclass
class CreateMessenger:
    """Returns a Messenger that has a queue."""

    queueu_url: Optional[str]
    queue_name: Optional[str]
    region_name: str
    delay_seconds: Optional[str]
    visibility_timeout: Optional[str]

    def return_messenger(self) -> Messenger:
        """Return a Messenger for an existing queue."""
        return Messenger(queueu_url=self.queueu_url, region=self.region_name)
'''
from pprint import pprint
import time
import boto3
from dataclasses import dataclass

from ezaws.sqs.models import ResponseMetadata


@dataclass
class GetQueueResponse:
    QueueUrl: str
    ResponseMetadata: ResponseMetadata


@dataclass
class CreateQueueResponse:
    QueueUrl: str
    ResponseMetadata: ResponseMetadata


@dataclass
class DeleteQueueResponse:
    ResponseMetadata: ResponseMetadata


def create_queue(queue_name: str) -> CreateQueueResponse:
    client = boto3.client("sqs", region_name="eu-central-1")
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


def delete_queue(queue_name: str) -> DeleteQueueResponse:
    sqs_client = boto3.client("sqs", region_name="eu-central-1")
    response = sqs_client.delete_queue(QueueUrl=queue_name)
    return DeleteQueueResponse(**response)


def purge_queue(queueu_url: str, region_name: str):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.purge_queue(QueueUrl=queueu_url)
    return response


def send_message(queueu_url: str, region_name: str, message: str):
    sqs_client = boto3.client("sqs", region_name=region_name)

    response = sqs_client.send_message(QueueUrl=queueu_url, MessageBody=message)
    return response


def receive_message(queueu_url: str, region_name: str, nr_of_messages: int = 1):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.receive_message(
        QueueUrl=queueu_url,
        MaxNumberOfMessages=nr_of_messages,  # max 10, default 1
        WaitTimeSeconds=0,
    )
    return response


def delete_message(queueu_url: str, region_name: str, receipt_handle: str):
    sqs_client = boto3.client("sqs", region_name=region_name)
    response = sqs_client.delete_message(
        QueueUrl=queueu_url,
        ReceiptHandle=receipt_handle,
    )

    return response


if __name__ == "__main__":
    queue_name = "example-queue"
    create_queue_resp = create_queue(queue_name)
    pprint(create_queue_resp)
    queue_url_resp = get_queue_url(queue_name)
    print("get queue response")
    pprint(queue_url_resp)
    val = input("Type 'delete' in case you want to delete the 'example-queue':")
    if val == "delete":
        delete_queu_response = delete_queue(queue_name)
        print("delete queue response")
        pprint(delete_queu_response)
    else:
        print("'example-queue' is not deleted.")
    queueu_url = "https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"
    region_name = "eu-central-1"

    print("Purging queue:")
    pugre_response = purge_queue(queueu_url=queueu_url, region_name=region_name)
    pprint(pugre_response)
    queueu_url = "https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"
    region_name = "eu-central-1"
    print("sending message:")
    send_response = send_message(
        queueu_url=queueu_url,
        region_name=region_name,
        message='{"important-key":"important-value-1"}',
    )
    pprint(send_response)
    time.sleep(2)
    receive_response = receive_message(
        queueu_url=queueu_url, region_name=region_name, nr_of_messages=10
    )

    send_message_id = send_response["MessageId"]
    send_message_md5 = send_response["MD5OfMessageBody"]
    print(
        f"\n\n\nMessage that was send to the queue has id {send_message_id} and md5 {send_message_md5}.\n\n"
    )

    to_delete = []
    print("Messages in the queue:")
    for msg in receive_response["Messages"]:
        pprint(msg)
        to_delete.append(msg["ReceiptHandle"])
    print(f"Deleting messages with the following receipt handles:")
    for item in to_delete:
        print(item)
    for receipt_handle in to_delete:

        delete_response = delete_message(
            queueu_url=queueu_url,
            region_name=region_name,
            receipt_handle=receipt_handle,
        )
        pprint(delete_response)
