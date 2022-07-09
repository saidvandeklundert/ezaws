from pprint import pprint
from ezaws import Region
from ezaws import DynamoDB
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if __name__ == "__main__":

    ddb = DynamoDB(region=Region.eu_central_1)
    result = ddb.get_item(table_name="Humans", item={"id": 1828, "name": "Arnetta"})

    pprint(result)
