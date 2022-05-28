import boto3
import botocore
from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
from botocore.exceptions import ClientError
from ezaws.models.dynamodb import (
    Table,
)
from typing import Union, Optional, List
from ezaws.exceptions import RDSException
from ezaws import Region


@dataclass
class DynamoDB:
    """
    Interface to the SSM Parameter store.
    """

    region: str
    dynamodb_client: botocore.client = boto3.client("dynamodb")

    def _create_table(self) -> None:
        """Creates a DynamoDB table"""
        dynamodb = boto3.resource("dynamodb")

        table = dynamodb.create_table(
            TableName="Humans",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
                {"AttributeName": "name", "KeyType": "RANGE"},  # Sort key
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "N"},
                {"AttributeName": "name", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },  # 1 RCU and 1 WCU is free!
        )

        print(
            f"Table Humans is in status {table.table_status}, waiting for \
                the table to be fully provisioned."
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Humans")
        state = dynamodb.Table("Humans").table_status
        print(f"Table created, status is now:{state}")

    def create_table(self, table: Table) -> None:
        """Creates a DynamoDB table"""
        dynamodb = boto3.resource("dynamodb")

        key_schema_list = []
        for key in table.keys.keys:
            key_schema_list.append(
                {"AttributeName": key.key_name, "KeyType": key.key_type}
            )
        attribute_list = []
        for attribute in table.attributes.attributes:
            attribute_list.append(
                {
                    "AttributeName": attribute.attribute_name,
                    "AttributeType": attribute.attribute_type,
                }
            )

        table = dynamodb.create_table(
            TableName=table.table_name,
            KeySchema=key_schema_list,
            AttributeDefinitions=attribute_list,
            ProvisionedThroughput={
                "ReadCapacityUnits": table.rcu,
                "WriteCapacityUnits": table.wcu,
            },  # 1 RCU and 1 WCU is free!
        )
        print("create table response:\n", table)
        print(
            f"Table Humans is in status {table.table_status}, waiting for \
                the table to be fully provisioned."
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Humans")
        state = dynamodb.Table("Humans").table_status
        print(f"Table created, status is now:{state}")
        return table

    def delete_table(self, table_name: str):
        """Deletes a DynamoDB table"""
        dynamodb = boto3.resource("dynamodb")

        table = dynamodb.Table(table_name)
        ret = table.delete()
        from pprint import pprint

        pprint(ret)


if __name__ == "__main__":
    table_d = {
        "table_name": "Humans",
        "attributes": {
            "attributes": [
                {"attribute_name": "id", "attribute_type": "N"},
                {"attribute_name": "name", "attribute_type": "S"},
            ]
        },
        "keys": {
            "keys": [
                {"key_name": "id", "key_type": "HASH"},
                {"key_name": "name", "key_type": "RANGE"},
            ]
        },
        "rcu": 1,
        "wcu": 1,
    }
    table = Table(**table_d)
    ddb = DynamoDB(region=Region.eu_central_1)
    table_response = ddb.create_table(table=table)
    print(table_response)
    import time

    time.sleep(20)
    ddb.delete_table(table_name=table.table_name)
