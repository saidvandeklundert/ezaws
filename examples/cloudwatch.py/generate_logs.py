from ezaws import Log, LogEvent
from pprint import pprint
import time
from uuid import uuid4


if __name__ == "__main__":

    cw_log = Log(name="cloudwatch_example", region="eu-central-1")

    # ez log:
    resp = cw_log.log(message="using log")
    pprint(resp)
    resp = cw_log.log_messages(
        messages=["using log_messages", "using log_messages again"],
    )
    pprint(resp)
    # log events

    events = [
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "event-1",
        },
        {
            "timestamp": int(round(time.time() * 1000)),
            "message": "even-2",
        },
        LogEvent(message="event-3", timestamp=int(round(time.time() * 1000))),
    ]
    resp = cw_log.log_events(events=events)
    pprint(resp)
    messages = []
    for i in range(100):
        messages.append("unique message" + str(uuid4()))
    cw_log.log_messages(
        messages=messages,
    )
