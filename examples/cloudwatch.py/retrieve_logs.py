from ezaws import Log
from pprint import pprint
import datetime
import time

if __name__ == "__main__":

    cw_log = Log(name="cloudwatch_example", region="eu-central-1")
    # grab everything
    resp = cw_log.get_log_events(limit=5000)
    pprint(resp)

    for event in resp.events:
        print(event.message)

        print(datetime.datetime.utcfromtimestamp(event.timestamp / 1000.0))

    # the last n minutes:
    print("Getting the last minutes.")
    resp = cw_log.get_log_events_last_minutes(minutes=1)
    pprint(resp)
    print("Getting the last hours.")
    resp = cw_log.get_log_events_last_hours(hours=2)
    pprint(resp)
    print("Getting the last seconds.")
    cw_log.log(message="just a few seconds ago")
    time.sleep(1)
    resp = cw_log.get_log_events_last_seconds(seconds=5)
    pprint(resp)
    for event in resp.events:
        # The Event has several fields/properties:
        # - message: the message that was logged to Cloudwatch
        # - timestamp: the timestap that is recorded in Cloudwatch:
        #       epoch in ms, which is the number of milliseconds
        #        after Jan 1, 1970
        # - date_time_local: the timestap converted to a
        #       datetime.datetime instance that represents the
        #        local time.
        # - epoch_local: date_time_local converted to the epoch in ms.
        print(event.message)
        print(event.timestamp)
        print(event.date_time_local)
        print(event.epoch_local)
