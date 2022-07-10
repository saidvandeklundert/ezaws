from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
from typing import Iterator, List, Optional, Any
from ezaws.utils.timing import (
    convert_to_local,
    epoch_to_date_time,
    datetime_to_epoch_in_ms,
)

import datetime


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

    def __iter__(self) -> Any:
        return iter(self.logStreams)


class LogEvent(BaseModel):
    timestamp: int  # number of milliseconds after Jan 1, 1970
    message: str  # message that should appear in CloudWatch logs


class Event(BaseModel):

    timestamp: int  # number of milliseconds after Jan 1, 1970
    message: str  # message that should appear in CloudWatch logs
    ingestionTime: Optional[int]

    @property
    def date_time_local(self) -> datetime.datetime:
        """Converts the epoch that is returned by Cloudwatch to
        a datetime.datetime object that represents the local time."""
        date_time = epoch_to_date_time(self.timestamp / 1000.0)
        local_date_time = convert_to_local(date_time)
        return local_date_time

    @property
    def epoch_local(self) -> int:
        """Converts the epoch that is returned by Cloudwatch to
        an epoch value that is representative of the local time."""
        date_time = epoch_to_date_time(self.timestamp / 1000.0)
        local_date_time = convert_to_local(date_time)
        local_epoch = datetime_to_epoch_in_ms(local_date_time)
        return local_epoch


class TailLogResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    events: List[Event]
    nextBackwardToken: str
    nextForwardToken: str

    def __iter__(self) -> Any:
        return iter(self.events)


class Events(BaseModel):
    events: List[Event] = []
