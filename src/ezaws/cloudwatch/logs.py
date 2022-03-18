import boto3
from botocore.exceptions import ClientError
from ezaws.models.cloudwatch import (
    CreateLogGroupResponse,
    DeleteLogGroupResponse,
    LogResponse,
    GetLogStreamRespone,
    Event,
    TailLogResponse,
    LogEvent,
)
from typing import Optional, Dict, NewType, Any, Union, List
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

    TODO:
    - dedup if not stream_name
    """

    name: str
    region: str
    default_stream_name: str = "general"
    streams: Dict[StreamName, Union[SequenceToken, None]] = Field(default_factory=dict)

    def __init__(self, **data: Any):
        """Think '__post_init__'"""
        super().__init__(**data)
        self.set_log_streams()

    def create_log_group(
        self, tags: Optional[Dict[str, str]] = None
    ) -> CreateLogGroupResponse:
        client = boto3.client("logs", region_name=self.region)
        args = {"logGroupName": self.name}
        if tags:
            args["tags"] = tags
        response = client.create_log_group(**args)
        return CreateLogGroupResponse(**response)

    def delete_log_group(self) -> DeleteLogGroupResponse:
        client = boto3.client("logs", region_name=self.region)
        response = client.delete_log_group(logGroupName=self.name)
        return DeleteLogGroupResponse(**response)

    def create_stream(self, stream_name: str) -> None:
        """Create a stream for this Cloudwatch logs instance."""
        client = boto3.client("logs", region_name=self.region)
        client.create_log_stream(logGroupName=self.name, logStreamName=stream_name)
        self.streams[stream_name] = None

    def log(
        self,
        *,
        message: str,
        stream_name: Optional[str] = None,
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
        stream_name: Optional[str] = None,
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
        events: List[Union[LogEvent, Dict]],
        stream_name: Optional[str] = None,
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
        if not stream_name:
            stream_name = self.default_stream_name
            if not stream_name in self.streams.keys():
                raise CloudWatchException(
                    f"default_stream_name {stream_name} does not exist."
                )
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
            log_event["sequenceToken"] = self.streams.get(stream_name)

        response = client.put_log_events(**log_event)

        ret = LogResponse(**response)

        self.streams[stream_name] = ret.nextSequenceToken
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
                self.streams[stream.logStreamName] = str(stream.uploadSequenceToken)
            else:
                self.streams[stream.logStreamName] = None
        return None

    def tail_log(
        self, n: int = 100, stream_name: Optional[str] = None
    ) -> TailLogResponse:
        """Look at latest n events in target stream.

        Checks the default stream if no stream_name is given."""
        if not stream_name:
            stream_name = self.default_stream_name
            if self.streams.get(stream_name) is None:
                raise CloudWatchException(
                    f"default_stream_name {stream_name} does not exist."
                )
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


if __name__ == "__main__":
    # TODO: move this to examples and sanitize
    cw_log = Log(name="creating_classs", region="eu-central-1")
    print(cw_log.dict())
    print("streams", cw_log.streams)
    """

    resp = cw_log.tail_log(10)
    pprint(resp)
    resp = cw_log.tail_log()
    pprint(resp)
    resp = cw_log.log_messages(
        messages=["multiple", "messages"],
    )
    print(resp)

    events = [
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "msg1",
        },
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "msg2",
        },
        LogEvent(message="tidbit", timestamp=int(round(time.time() * 1000))),
    ]
    resp = cw_log.log_events(events=events)
    pprint(resp)

    resp = cw_log.log(
        stream_name="application",
        message="YOLO",
    )

    print("streams", cw_log.streams)
    resp = cw_log.log(
        stream_name="application",
        message="YOLO",
    )
    print(resp)
    resp = cw_log.log(message="YOLO",)
    print(resp)

    resp = cw_log.log_messages(
        messages=["multiple", "messages"],
    )
    print(resp)


    print(resp)
    

    
    cw_log.create_stream(stream_name="general")
    
    resp = cw_log.get_log_streams()
    pprint(resp)
    
    cw_log.log(
        stream_name="application",
        message="YOLO",
        seq_token="49627245584982296427518639517447485581149901951829520338",
    )
    
    resp = cw_log.create_log_group()
    pprint(resp)
    
    resp = cw_log.create_stream("application")
    pprint(resp)
    
    resp = cw_log.delete_log_group()
    pprint(resp)
    
    
    
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
    """
