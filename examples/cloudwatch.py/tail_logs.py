from ezaws import Log
from pprint import pprint
import datetime

if __name__ == "__main__":

    cw_log = Log(name="cloudwatch_example", region="eu-central-1")

    resp = cw_log.tail_log(10)
    pprint(resp)
    resp = cw_log.tail_log()
    pprint(resp)
    for log in resp:
        print(log.message)
        print(log.timestamp)
        sec = log.timestamp / 1000.0
        print(datetime.datetime.utcfromtimestamp(sec))
