"""
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.send_message
"""
from pprint import pprint
import boto3
from dataclasses import dataclass
from typing import Dict, List, Optional, TypeVar
from ezaws.sqs.models import (
    DeleteQueueResponse,
    CreateQueueResponse,
    ListQueueResponse,
    GetQueueResponse,
    SendMessageResponse,
    ReadMessageResponse,
    PurgeQueueResponse,
    QueueAttributes,
    Message,
)

T = TypeVar("T", bound="Messenger")


# Functions:


def delete_queue(queue_name: str, region: str) -> DeleteQueueResponse:
    sqs_client = boto3.client("sqs", region_name=region)
    response = sqs_client.delete_queue(QueueUrl=queue_name)
    return DeleteQueueResponse(**response)


def list_queues(region: str, max_results=100) -> ListQueueResponse:
    """Returns a list of URLs inside a ListQueueResponse,
    listing all the queues in a region."""
    sqs_client = boto3.client("sqs", region_name=region)
    response = sqs_client.list_queues(MaxResults=max_results)
    return ListQueueResponse(**response)


# TODO: add read_all() method


@dataclass
class Messenger:

    queueu_url: str
    region: str

    @classmethod
    def from_queue_name(
        cls,
        queue_name: str,
        region: str,
        delay_seconds: str = "0",
        visibility_timeout: str = "30",
    ) -> T:
        """Returns a Messenger for a region from a 'queue_name'.

        If the queue already exists, that queue is returned. If the
         queue does not exist already, a new queue is created.

        Example:
            >>> x = Messenger.from_queue_name("some_queue", region="eu-central-1")
        """
        list_q_response = cls._list_queues(region, max_results=100)
        for url in list_q_response:
            if url.endswith(queue_name):
                sqs_client = boto3.client("sqs", region_name=region)
                response: GetQueueResponse = sqs_client.get_queue_url(
                    QueueName=queue_name,
                )
                return Messenger(queueu_url=response.QueueUrl, region=region)
        client = boto3.client("sqs", region_name=region)
        response = client.create_queue(
            QueueName=queue_name,
            Attributes={
                "DelaySeconds": delay_seconds,  # default 0, max 900 (15 min)
                "VisibilityTimeout": visibility_timeout,  # default 30, min 0
            },
        )
        response = CreateQueueResponse(**response)
        return Messenger(queueu_url=response.QueueUrl, region=region)

    def _get_queue_url(
        self,
        queue_name: str,
        region_name: str,
        delay_seconds: str = "0",
        visibility_timeout: str = "30",
    ) -> str:
        """Returns a queue with target name for the region.

        Creates the queue if it does not already exist."""
        list_queue_response = self._list_queues()
        for q_url in list_queue_response:
            if queue_name in q_url:
                # queue exists, so we return the queueu url:
                return queue_name
        client = boto3.client("sqs", region_name=region_name)
        response = client.create_queue(
            QueueName=queue_name,
            Attributes={
                "DelaySeconds": delay_seconds,  # default 0, max 900 (15 min)
                "VisibilityTimeout": visibility_timeout,  # default 30, min 0
            },
        )
        response = CreateQueueResponse(**response)
        return response.QueueUrl

    def send_message(self, message: str) -> SendMessageResponse:
        """Send a message to the queue."""
        sqs_client = boto3.client("sqs", region_name=self.region)

        response = sqs_client.send_message(
            QueueUrl=self.queueu_url, MessageBody=message
        )
        return SendMessageResponse(**response)

    def read_messages(self, nr_of_messages: int = 1) -> ReadMessageResponse:
        """Read a number of messages from the queue."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.receive_message(
            QueueUrl=self.queueu_url,
            MaxNumberOfMessages=nr_of_messages,  # max 10, default 1
            WaitTimeSeconds=0,
        )
        return ReadMessageResponse(**response)

    def delete_message(self, receipt_handle: str):
        """Delete target message from the queueu"""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.delete_message(
            QueueUrl=self.queueu_url,
            ReceiptHandle=receipt_handle,
        )
        return response

    def get_queue_count(self) -> int:
        """Returns the 'ApproximateNumberOfMessages' from the queueu."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.get_queue_attributes(
            QueueUrl=self.queueu_url,
            AttributeNames=["ApproximateNumberOfMessages"],
        )

        return response["Attributes"]["ApproximateNumberOfMessages"]

    def get_queue_attributes(self) -> QueueAttributes:
        """Returns the queueu attributes."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.get_queue_attributes(
            QueueUrl=self.queueu_url,
            AttributeNames=["All"],
        )
        ret = QueueAttributes(**response["Attributes"])
        return ret

    def purge_queue(self):
        """Purge the queue."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.purge_queue(QueueUrl=self.queueu_url)

        return PurgeQueueResponse(**response)

    def _list_queues(region: str, max_results=100) -> ListQueueResponse:
        """Returns a list of URLs inside a ListQueueResponse,
        listing all the queues in a region."""
        sqs_client = boto3.client("sqs", region_name=region)

        response = sqs_client.list_queues(MaxResults=max_results)
        return ListQueueResponse(**response)


if __name__ == "__main__":

    msgnr = Messenger(
        queueu_url="https://eu-central-1.queue.amazonaws.com/717687450252/example-queue",
        region="eu-central-1",
    )
    # msgnr._list_queues("eu-central-1")
    print(msgnr.get_queue_count())
    print(msgnr.get_queue_attributes())

    msg = msgnr.send_message("message 1")
    msg = msgnr.send_message("message 2")
    msg = msgnr.send_message("message 3")
    msg = msgnr.send_message("message 4")
    msg = msgnr.send_message("message 5")

    msg_read = msgnr.read_messages(nr_of_messages=10)

    for m in msg_read:
        m = Message(**m)
        print(f"read message {m.Body}")
        msgnr.delete_message(receipt_handle=m.ReceiptHandle)

    print(msgnr.get_queue_count())
    pprint(vars(msgnr.get_queue_attributes()))
