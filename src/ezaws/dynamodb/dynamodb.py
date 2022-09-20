import boto3
import botocore
from boto3.dynamodb.conditions import Key
from dataclasses import dataclass
from ezaws.models.dynamodb import (
    DeleteResponse,
    Table,
    GetItemResponse,
    ScanResult,
    PartiQLResult,
)
from typing import List, Any, Dict
import logging

logger = logging.getLogger(__name__)


@dataclass
class DynamoDB:
    """
    Interface to DynamoDB
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

        created_table = dynamodb.create_table(
            TableName=table.table_name,
            KeySchema=key_schema_list,
            AttributeDefinitions=attribute_list,
            ProvisionedThroughput={
                "ReadCapacityUnits": table.rcu,
                "WriteCapacityUnits": table.wcu,
            },  # 1 RCU and 1 WCU is free!
        )
        logger.info(
            f"Table {created_table.table_name} is in status {created_table.table_status}"
            "\nWaiting for the table to be fully provisioned."
        )

        created_table.meta.client.get_waiter("table_exists").wait(
            TableName=table.table_name
        )
        state = dynamodb.Table(table.table_name).table_status
        logger.info(f"Table created, status is now:{state}")

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

    def scan(self, table_name: str) -> ScanResult:
        """Scan target table"""
        scan_result = self.ddb_client.scan(TableName=table_name)
        return ScanResult(**scan_result)

    def ez_scan(self, table_name: str) -> list[Any]:
        result = self.ddb_client.scan(table_name=table_name)
        deserializer = boto3.dynamodb.types.TypeDeserializer()

        def deserialize(d: dict) -> dict:
            return {k: deserializer.deserialize(v) for k, v in d.items()}

        data = [deserialize(d) for d in result.Items]
        return data

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
        """Return a list of table objects (boto3.resources.factory.dynamodb.Table)
        for the region"""
        tables = list(self.ddb_resource.tables.all())
        return tables

    def list_table_names(self) -> List[str]:
        """Return a list of table names for the region"""
        tables = list(self.ddb_resource.tables.all())

        tables = [table.table_name for table in tables]

        return tables

    #    def query(self, table_name: str) -> QueryResult:
    #        dynamo_db = boto3.resource("dynamodb")
    #        table = dynamo_db.Table(table_name)
    #        response = table.query(KeyConditionExpression=Key("id").eq(10))
    #        result = QueryResult(**response)
    #        return result

    def partiql_query(self, partiql_query: str) -> PartiQLResult:
        """
        Execute a PartiQL query against Dynamo.

        For information on using PartiQL, check
         https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-reference.html
        """
        logger.info(f"Executing partiql query {partiql_query}\n")
        result = self.ddb_client.execute_statement(Statement=partiql_query)
        return PartiQLResult(**result)
