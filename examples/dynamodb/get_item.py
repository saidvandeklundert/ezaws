from pprint import pprint
from ezaws import Region
from ezaws import DynamoDB


if __name__ == "__main__":

    ddb = DynamoDB(region=Region.eu_central_1)
    result = ddb.get_item(table_name="Humans", item={"id": 99, "name": "Arnetta"})

    pprint(result)
