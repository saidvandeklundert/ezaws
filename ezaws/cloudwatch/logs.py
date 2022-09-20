import boto3
from ezaws.utils.timing import (
    epoch_minutes_ago,
    epoch_days_ago,
    epoch_seconds_ago,
    epoch_hours_ago,
)
from botocore.exceptions import ClientError
from ezaws.models.cloudwatch import (
    CreateLogGroupResponse,
    DeleteLogGroupResponse,
    LogResponse,
    GetLogStreamRespone,
    Event,
    TailLogResponse,
    LogEvent,
    Events,
)
from typing import Optional, Dict, NewType, Any, Sequence, Union, List
from pprint import pprint
import time
from pydantic import BaseModel, Field

from typing_extensions import TypedDict
from ezaws.exceptions import CloudWatchException

StreamName = NewType("StreamName", str)
SequenceToken = NewType("SequenceToken", str)
StreamDict = TypedDict(
    "StreamDict",
    {
        "StreamName": StreamName,
        "SequenceToken": Union[SequenceToken, None],
    },
)


class Log(BaseModel):
    """Interface to Cloudwatch Logs.

    The Log represents a single log group in a region. It can
     perform most common operations, such as:
    - create the log group
    - create streams
    - retrieve logs


    name: name of the log group
    region: the region the log is in
    default_stream_name: name of the stream to log to when the stream name is not
     passed in as an argument to logging functions
    streams: the streams that have been created for the log group
    """

    name: str
    region: str
    default_stream_name: StreamName = "general"  # type: ignore
    streams: Dict[StreamName, Union[SequenceToken, None]] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        """Think '__post_init__'"""
        super().__init__(**data)
        self.set_log_streams()

    def create_log_group(
        self, tags: Optional[Dict[str, str]] = None
    ) -> CreateLogGroupResponse:
        client = boto3.client("logs", region_name=self.region)
        args: dict[str, Any] = {"logGroupName": self.name}
        if tags:
            args["tags"] = tags
        response = client.create_log_group(**args)
        return CreateLogGroupResponse(**response)

    def delete_log_group(self) -> DeleteLogGroupResponse:
        client = boto3.client("logs", region_name=self.region)
        response = client.delete_log_group(logGroupName=self.name)
        return DeleteLogGroupResponse(**response)

    def create_stream(self, stream_name: StreamName) -> None:
        """Create a stream for this Cloudwatch logs instance."""
        client = boto3.client("logs", region_name=self.region)
        client.create_log_stream(logGroupName=self.name, logStreamName=stream_name)
        self.streams[stream_name] = None

    def log(
        self,
        *,
        message: str,
        stream_name: Optional[StreamName] = None,
    ) -> LogResponse:
        """Log a message to a stream.

        Use the default stream is the stream name is not specified."""

        events = [
            LogEvent(message=message, timestamp=int(round(time.time() * 1000))),
        ]
        resp = self.log_events(events=events, stream_name=stream_name)

        return resp

    def log_messages(
        self,
        *,
        messages: List[str],
        stream_name: Optional[StreamName] = None,
    ) -> LogResponse:
        """Log multiple message to a stream.

        Use the default stream is the stream name is not specified."""

        events = []
        for message in messages:
            events.append(
                {
                    "timestamp": int(round(time.time() * 1000)),
                    "message": message,
                }
            )
        resp = self.log_events(events=events, stream_name=stream_name)
        return resp

    def log_events(
        self,
        *,
        events: Sequence[Union[LogEvent, Dict]],
        stream_name: Optional[StreamName] = None,
    ) -> LogResponse:
        """Log multiple message to a stream.

        Use the default stream is the stream name is not specified.

        The events can either be a of the type Event, or they can be dicts,
         like so:
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "msg1",
        }
        """
        if stream_name is None:
            stream_name = self._get_stream_name()
        client = boto3.client("logs", region_name=self.region)
        # pprint(events)
        events_to_log = list(
            event.dict() for event in events if isinstance(event, LogEvent)
        )
        events_to_log.extend(
            list((event for event in events if isinstance(event, dict)))
        )
        # pprint(events)
        log_event = {
            "logGroupName": self.name,
            "logStreamName": stream_name,
            "logEvents": events_to_log,
        }

        if self.streams.get(stream_name) is not None:
            log_event["sequenceToken"] = self.streams.get(stream_name)  # type: ignore

        response = client.put_log_events(**log_event)

        ret = LogResponse(**response)
        token: SequenceToken = ret.nextSequenceToken  # type: ignore
        self.streams[stream_name] = token
        return ret

    def get_log_streams(
        self,
    ) -> GetLogStreamRespone:
        """Retrieve and store information from all streams for this log group"""
        client = boto3.client("logs", region_name=self.region)
        response = client.describe_log_streams(
            logGroupName=self.name,
        )
        print(response)
        return GetLogStreamRespone(**response)

    def set_log_streams(self) -> None:
        """Retrieve all log streams for this log group and set the next token."""
        try:
            resp = self.get_log_streams()
        except ClientError as e:
            if e.response["Error"]["Code"] == "ResourceNotFoundException":
                # this means that we do not have any streams yet.
                return None
            raise e

        for stream in resp:
            # print(stream.uploadSequenceToken, stream.logStreamName)
            if isinstance(stream.uploadSequenceToken, int):
                self.streams[stream.logStreamName] = str(stream.uploadSequenceToken)  # type: ignore
            else:
                self.streams[stream.logStreamName] = None
        return None

    def _get_stream_name(self) -> StreamName:
        """Helper to return the default stream name
        and raise an exception in case it does not exist.
        """
        stream_name = self.default_stream_name
        if stream_name not in self.streams.keys():
            raise CloudWatchException(
                f"default_stream_name {stream_name} does not exist. Existing streams:\n{self.streams}"
            )
        return stream_name

    def tail_log(
        self, n: int = 100, stream_name: Optional[str] = None
    ) -> TailLogResponse:
        """Look at latest n events in target stream.

        Checks the default stream if no stream_name is given."""
        if stream_name is None:
            stream_name = self._get_stream_name()
        client = boto3.client("logs", region_name=self.region)

        response = client.get_log_events(
            logGroupName=self.name,
            logStreamName=stream_name,
            # startTime=int(datetime.datetime(2021, 8, 19, 0, 0).strftime('%s'))*1000,
            # endTime=int(datetime.datetime(2021, 8, 20, 0, 0).strftime('%s'))*1000,
            limit=n,
            startFromHead=False,
        )
        return TailLogResponse(**response)

    def get_log_events(
        self,
        stream_name: Optional[str] = None,
        limit: int = 10,
        startTime: Optional[int] = None,
        endTime: Optional[int] = None,
        start_from_head: bool = True,
    ) -> Events:
        """Retrieve the entire log and returns it.

        Checks the default stream if no stream_name is given.

        Returns all the events for the log.

        The last item in the list is the newest event.

        Notes to self:

          - when startFromHead is set to True, it reads the oldest logs first.

          - when startFromHead is set to False, it reads the newest logs first.

          - using 'nextForwardToken' is moving from old to new logs.

          - using 'nextBackwardToken' is moving from new to old logs.
        """
        if stream_name is None:
            stream_name = self._get_stream_name()
        client = boto3.client("logs", region_name=self.region)
        events = Events()
        get_log_events_kwargs = {
            "logGroupName": self.name,
            "logStreamName": stream_name,
            "limit": limit,
            "startFromHead": start_from_head,
        }
        if startTime:
            get_log_events_kwargs["startTime"] = startTime

        if endTime:
            get_log_events_kwargs["endTime"] = endTime

        response = client.get_log_events(**get_log_events_kwargs)
        response = TailLogResponse(**response)
        for event in response.events:
            events.events.append(event)

        # print(response.nextBackwardToken)
        # print(response.nextForwardToken)

        next_token = response.nextForwardToken
        while True:
            get_log_events_kwargs["nextToken"] = next_token
            response = client.get_log_events(**get_log_events_kwargs)
            response = TailLogResponse(**response)
            for event in response.events:
                events.events.append(event)
                print(event)
            # The log is depleted when AWS starts returning
            # the same token over and over.
            if next_token == response.nextForwardToken:
                break
            else:
                next_token = response.nextForwardToken

        return events

    def get_log_events_last_seconds(self, seconds: int) -> Events:
        epoch_seconds = epoch_seconds_ago(seconds)
        events = self.get_log_events(
            limit=5000, startTime=epoch_seconds, start_from_head=True
        )
        return events

    def get_log_events_last_minutes(self, minutes: int) -> Events:
        epoch_minutes = epoch_minutes_ago(minutes)
        events = self.get_log_events(
            limit=5000, startTime=epoch_minutes, start_from_head=True
        )
        return events

    def get_log_events_last_hours(self, hours: int) -> Events:
        epoch_hours = epoch_hours_ago(hours)
        events = self.get_log_events(
            limit=5000, startTime=epoch_hours, start_from_head=True
        )
        return events

    def get_log_events_last_days(self, days: int) -> Events:
        epoch_days = epoch_days_ago(days)
        events = self.get_log_events(
            limit=5000, startTime=epoch_days, start_from_head=True
        )
        return events
