from pprint import pprint
import csv
from ezaws import Region
from ezaws import DynamoDB

MAX = 200

if __name__ == "__main__":
    ddb = DynamoDB(region=Region.eu_central_1)
    result = ddb.scan(table_name="Humans")
    pprint(result)
    items = [
        {"id": 1, "name": "Said van de Klundert", "age": 38},
        {
            "id": 2,
            "name": "Jan van de Klundert",
        },
        {
            "id": 3,
            "name": "Marie van de Klundert",
        },
        {
            "id": 4,
            "name": "Anne van de Klundert",
        },
    ]
    ddb.put_items(table_name="Humans", items=items)
    ddb.put_item(table_name="Humans", item={"id": 5, "name": "Henk"})

    with open("data/names.csv", "rt") as f:
        csv_data = csv.DictReader(f)

        for row in csv_data:
            print(row)
            if MAX:
                ddb.put_item(
                    table_name="Humans",
                    item={"id": int(row["id"]), "name": row["name"]},
                )
                MAX -= 1
            else:
                break
    result = ddb.scan(table_name="Humans")
    pprint(result)
