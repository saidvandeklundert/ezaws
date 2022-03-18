from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
from typing import List, Optional


class CreateLogGroupResponse(BaseModel):
    ResponseMetadata: ResponseMetadata


class DeleteLogGroupResponse(BaseModel):
    ResponseMetadata: ResponseMetadata


class LogResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    nextSequenceToken: str


class LogStreams(BaseModel):
    """Individual stream inside a log group."""

    arn: str
    creationTime: int
    firstEventTimestamp: Optional[int]
    lastEventTimestamp: Optional[int]
    lastIngestionTime: Optional[int]
    logStreamName: str
    storedBytes: int
    uploadSequenceToken: Optional[int]


class GetLogStreamRespone(BaseModel):
    ResponseMetadata: ResponseMetadata
    logStreams: List[LogStreams]

    def __iter__(self):
        return iter(self.logStreams)


class LogEvent(BaseModel):
    timestamp: int  # number of milliseconds after Jan 1, 1970
    message: str  # message that should appear in CloudWatch logs


class Event(BaseModel):
    timestamp: int  # number of milliseconds after Jan 1, 1970
    message: str  # message that should appear in CloudWatch logs
    ingestionTime: Optional[int]


class TailLogResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    events: List[Event]
    nextBackwardToken: str
    nextForwardToken: str

    def __iter__(self):
        return iter(self.events)
