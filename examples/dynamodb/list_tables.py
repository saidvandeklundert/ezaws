from pprint import pprint
from ezaws import Region
from ezaws import DynamoDB

if __name__ == "__main__":

    ddb = DynamoDB(region=Region.eu_central_1)
    result = ddb.list_tables()

    pprint(result)

    result = ddb.list_table_names()
    pprint(result)
