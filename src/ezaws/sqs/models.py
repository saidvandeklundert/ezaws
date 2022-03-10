from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class QueueAttributes:
    ApproximateNumberOfMessages: int
    ApproximateNumberOfMessagesDelayed: int
    ApproximateNumberOfMessagesNotVisible: int
    CreatedTimestamp: int
    DelaySeconds: int
    LastModifiedTimestamp: int
    MaximumMessageSize: int
    MessageRetentionPeriod: int
    QueueArn: str
    ReceiveMessageWaitTimeSeconds: int
    SqsManagedSseEnabled: bool
    VisibilityTimeout: int


@dataclass
class Message:
    MessageId: str
    ReceiptHandle: str
    MD5OfBody: str
    Body: str  # the actual message


@dataclass
class ResponseMetadata:
    RequestId: str
    HTTPStatusCode: str
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int


@dataclass
class ReadMessageResponse:
    ResponseMetadata: ResponseMetadata
    Messages: List[Message] = field(default_factory=list)

    def __iter__(self):
        return iter(self.Messages)


@dataclass
class ResponseMetadata:
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: Optional[int]


@dataclass
class SendMessageResponse:
    MD5OfMessageBody: str
    MessageId: str
    ResponseMetadata: ResponseMetadata


@dataclass
class DeleteResponse:
    ResponseMetadata: ResponseMetadata
    RequestId: str
    HTTPStatusCode: int
    RetryAttempts: int
    HTTPHeaders: Dict[str, str] = field(default_factory=dict)


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


@dataclass
class ListQueueResponse:
    # ["https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"]
    QueueUrls: List[str]
    ResponseMetadata: ResponseMetadata

    def __iter__(self):
        return iter(self.QueueUrls)


class PurgeQueueResponse:
    ResponseMetadata: ResponseMetadata
