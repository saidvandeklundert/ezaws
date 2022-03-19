from ezaws import Log
from pprint import pprint

if __name__ == "__main__":

    cw_log = Log(name="cloudwatch_example", region="eu-central-1")
    resp = cw_log.create_log_group()
    pprint(resp)
    resp = cw_log.create_stream(stream_name="general")
    pprint(resp)
    resp = cw_log.get_log_streams()
    pprint(resp)
