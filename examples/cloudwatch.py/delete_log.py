from ezaws import Log
from pprint import pprint

if __name__ == "__main__":

    cw_log = Log(name="cloudwatch_example", region="eu-central-1")
    resp = cw_log.delete_log_group()
    pprint(resp)
