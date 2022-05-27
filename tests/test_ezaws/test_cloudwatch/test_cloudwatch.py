from ezaws import Log
import time
from ezaws.models.cloudwatch import (
    CreateLogGroupResponse,
    DeleteLogGroupResponse,
    Events,
    LogResponse,
    LogEvent,
    TailLogResponse,
)


def test_create_log_group():
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    resp = cw_log.create_log_group()
    assert isinstance(resp, CreateLogGroupResponse)


def test_create_stream():
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    cw_log.create_stream(stream_name="general")
    assert "general" in cw_log.streams.keys()


def test_log_events():
    """Log a few events"""
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    events = [
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "test_log_events",
        },
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "test_log_events",
        },
        LogEvent(message="tidbit", timestamp=int(round(time.time() * 1000))),
    ]
    resp = cw_log.log_events(events=events)
    assert isinstance(resp, LogResponse)


def test_log():
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    resp = cw_log.log(message="test_log")
    assert isinstance(resp, LogResponse)


def test_log_messages():
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    resp = cw_log.log_messages(
        messages=["test_log_messages", "test_log_messages"],
    )
    assert isinstance(resp, LogResponse)


def test_get_log_events():
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    resp_list = []
    resp_list.append(cw_log.get_log_events_last_seconds(seconds=5))
    resp_list.append(cw_log.get_log_events_last_minutes(minutes=5))
    resp_list.append(cw_log.get_log_events_last_hours(hours=5))
    resp_list.append(cw_log.get_log_events_last_days(days=5))
    for resp in resp_list:
        assert isinstance(resp, Events)


def test_tail_log():
    """test the tail_log method as well as the reception of previously
    generated logs."""
    cw_log = Log(name="testing_log_group", region="eu-central-1")

    resp = cw_log.tail_log(n=200)
    assert isinstance(resp, TailLogResponse)
    messages = []
    for event in resp:
        messages.append(event.message)
    print(messages)
    # time.sleep(3)
    assert "test_log_events" in messages
    assert "test_log_messages" in messages
    assert "test_log" in messages


def test_delete_log_group():
    cw_log = Log(name="testing_log_group", region="eu-central-1")
    resp = cw_log.delete_log_group()
    assert isinstance(resp, DeleteLogGroupResponse)
