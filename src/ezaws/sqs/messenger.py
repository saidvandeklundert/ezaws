import boto3
from dataclasses import dataclass
from typing import Any
from ezaws.models.sqs import (
    DeleteQueueResponse,
    CreateQueueResponse,
    ListQueueResponse,
    GetQueueResponse,
    DeleteMessageResponse,
    SendMessageResponse,
    ReadMessageResponse,
    PurgeQueueResponse,
    QueueAttributes,
)


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
    ) -> Any:
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
                response = sqs_client.get_queue_url(
                    QueueName=queue_name,
                )
                response = GetQueueResponse(**response)
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

        list_queue_response = self._list_queues(region_name)
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
        create_queue_response = CreateQueueResponse(**response)
        return create_queue_response.QueueUrl

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

    def delete_message(self, receipt_handle: str) -> DeleteMessageResponse:
        """Delete target message from the queueu"""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.delete_message(
            QueueUrl=self.queueu_url,
            ReceiptHandle=receipt_handle,
        )
        return DeleteMessageResponse(**response)

    def get_queue_count(self) -> int:
        """Returns the 'ApproximateNumberOfMessages' from the queueu."""

        return int(self.get_queue_attributes().ApproximateNumberOfMessages)

    def get_queue_attributes(self) -> QueueAttributes:
        """Returns the queueu attributes."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.get_queue_attributes(
            QueueUrl=self.queueu_url,
            AttributeNames=["All"],
        )
        ret = QueueAttributes(**response["Attributes"])
        return ret

    def purge_queue(self) -> PurgeQueueResponse:
        """Purge the queue."""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.purge_queue(QueueUrl=self.queueu_url)

        return PurgeQueueResponse(**response)

    def delete_queue(self) -> DeleteQueueResponse:
        """Deletes the queue"""
        sqs_client = boto3.client("sqs", region_name=self.region)
        response = sqs_client.delete_queue(QueueUrl=self.queueu_url)
        return DeleteQueueResponse(**response)

    @staticmethod
    def _list_queues(region: str, max_results: int = 100) -> ListQueueResponse:
        """Returns a list of URLs inside a ListQueueResponse,
        listing all the queues in a region."""

        sqs_client = boto3.client("sqs", region_name=region)

        response = sqs_client.list_queues(MaxResults=max_results)
        return ListQueueResponse(**response)
