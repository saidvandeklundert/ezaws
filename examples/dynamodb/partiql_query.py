from pprint import pprint
from ezaws import Region
from ezaws import DynamoDB
import logging

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

if __name__ == "__main__":

    ddb = DynamoDB(region=Region.eu_central_1)
    pprint(ddb.partiql_query("SELECT * FROM Humans"))
    pprint(ddb.partiql_query("SELECT name FROM Humans WHERE name ='x'"))
    pprint(ddb.partiql_query("SELECT name FROM Humans WHERE id =1"))
    pprint(ddb.partiql_query("SELECT * FROM Humans WHERE id =7"))
