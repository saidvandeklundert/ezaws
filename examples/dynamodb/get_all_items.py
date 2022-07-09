from pprint import pprint
from ezaws import Region
from ezaws import DynamoDB


if __name__ == "__main__":

    ddb = DynamoDB(region=Region.eu_central_1)
    result = ddb.scan(table_name="Humans")

    pprint(result)
