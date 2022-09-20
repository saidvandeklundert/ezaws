from pprint import pprint
from ezaws import Region
from ezaws import DynamoDB, Table
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if __name__ == "__main__":

    table = Table(table_name="Humans", rcu=1, wcu=1)
    table.add_attribute(attribute_name="id", attribute_type="N", key_type="HASH")
    table.add_attribute(attribute_name="name", attribute_type="S", key_type="RANGE")
    ddb = DynamoDB(region=Region.eu_central_1)
    table_response = ddb.create_table(table=table)
    pprint(table_response)
