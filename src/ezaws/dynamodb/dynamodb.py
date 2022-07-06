from pprint import pprint
import boto3
import botocore
from pydantic import BaseModel
from enum import Enum
from dataclasses import dataclass
from botocore.exceptions import ClientError
from ezaws.models.dynamodb import DeleteResponse, Table, GetItemResponse, Keys
from typing import Union, Optional, List, Any, Dict
from ezaws.exceptions import RDSException
from ezaws import Region


@dataclass
class DynamoDB:
    """
    Interface to Dyanmo
    """

    region: str
    ddb_client: botocore.client = boto3.client("dynamodb")
    ddb_resource: boto3.resource = boto3.resource("dynamodb")

    def create_table(self, table: Table) -> bool:
        """Creates a DynamoDB table"""
        dynamodb = boto3.resource("dynamodb")

        key_schema_list = []
        for key in table.keys:
            key_schema_list.append(
                {"AttributeName": key.key_name, "KeyType": key.key_type}
            )
        attribute_list = []
        for attribute in table.attributes:
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
            f"Table {table.table_name} is in status {table.table_status}, waiting for \
                the table to be fully provisioned."
        )
        table.meta.client.get_waiter("table_exists").wait(TableName="Humans")
        state = dynamodb.Table("Humans").table_status
        print(f"Table created, status is now:{state}")
        return True

    def delete_table(self, table_name: str) -> DeleteResponse:
        """Deletes a DynamoDB table"""
        dynamodb = boto3.resource("dynamodb")

        table = dynamodb.Table(table_name)
        ret = table.delete()

        return DeleteResponse(**ret)

    def put_items(self, table_name: str, items: List[Dict[Any, Any]]) -> bool:
        """Add a list of items to target table."""

        for item in items:
            self.put_item(table_name=table_name, item=item)
        return True

    def put_item(self, table_name: str, item: Dict[Any, Any]) -> bool:
        """Add an item to target table."""
        table = self.ddb_resource.Table(table_name)
        table.put_item(Item=item)
        return True

    def scan(self, table_name: str):
        """Scan target table"""
        scan_result = self.ddb_client.scan(TableName=table_name)
        return scan_result

    def get_item(self, table_name: str, item: Dict[Any, Any]) -> GetItemResponse:
        """Get item from target table.

        Example:

        >>> ddb.get_item(
            table_name="Humans",
            item={"id": 1828, "name": "Arnetta"},
            )


        """
        table = self.ddb_resource.Table(table_name)
        get_item_result = table.get_item(Key=item)

        return GetItemResponse(**get_item_result)

    def list_tables(self) -> List[Any]:
        """Return a list of table objects for the region"""
        tables = list(self.ddb_resource.tables.all())

        return tables

    def list_table_names(self) -> List[str]:
        """Return a list of table names for the region"""
        tables = list(self.ddb_resource.tables.all())

        tables = [table.table_name for table in tables]

        return tables

    '''
    def quarey(self):
        """"""
        dynamo_db = boto3.resource("dynamodb")
        table = dynamo_db.Table("devices")
        response = table.query(KeyConditionExpression=Key("name").eq("core02-wdc01"))
        for item in response["Items"]:
            pprint(item)
    '''


if __name__ == "__main__":

    ddb = DynamoDB(region=Region.eu_central_1)
    result = ddb.get_item(table_name="Humans", item={"id": 1828, "name": "Arnetta"})

    pprint(result)
