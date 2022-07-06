from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
from enum import Enum

from typing import Union, Optional, List, Literal, Dict, Any


class AttributeType(Enum):
    S = "S"  # string
    N = "N"  # number
    B = "B"  # binary


class Attribute(BaseModel):
    attribute_name: str
    attribute_type: AttributeType

    class Config:
        use_enum_values = True


class Attributes(BaseModel):
    attributes: List[Attribute]

    def iter(self):
        return iter(self.attributes)


class Key(Enum):
    HASH = "HASH"  # partition key
    RANGE = "RANGE"  # sort key


class KeySchema(BaseModel):
    key_name: str
    key_type: Key

    class Config:
        use_enum_values = True


class Keys(BaseModel):
    keys: List[KeySchema]

    def iter(self):
        return iter(self.keys)


class Table(BaseModel):
    table_name: str
    attributes: List[Attributes] = []
    keys: List[Keys] = []
    rcu: int  # ReadCapacityUnits: 1 is free
    wcu: int  # WriteCapacityUnits: 1 is free

    def add_attribute(
        self,
        attribute_name: str,
        attribute_type: Literal["S", "N", "B"],
        key_type: Literal["HASH", "RANGE"],
    ) -> None:
        """Add an attribute to the Table and define the attribute type and key.

        Attribute types:
            "S" for string
            "N" for number
            "B" for binary

        Attribute key types:
            "HASH" for partition key
            "RANGE" for sort key
        """
        attribute = Attribute(
            attribute_name=attribute_name, attribute_type=attribute_type
        )
        key_schema = KeySchema(key_name=attribute_name, key_type=key_type)
        self.attributes.append(attribute)
        self.keys.append(key_schema)


class ProvisionedThroughput(BaseModel):
    NumberOfDecreasesToday: int
    ReadCapacityUnits: int
    WriteCapacityUnits: int


class TableDescription(BaseModel):
    ItemCount: int
    ProvisionedThroughput: ProvisionedThroughput
    TableArn: str
    TableId: str
    TableName: str
    TableSizeBytes: int
    TableStatus: str


class DeleteResponse(BaseModel):
    ResponseMetadata: ResponseMetadata
    TableDescription: TableDescription


class GetItemResponse(BaseModel):
    Item: dict
    ResponseMetadata: ResponseMetadata


if __name__ == "__main__":
    attributes = Attributes(
        attributes=[
            Attribute(attribute_name="id", attribute_type=AttributeType.N),
            Attribute(attribute_name="name", attribute_type=AttributeType.S),
        ]
    )
    keys = Keys(
        keys=[
            KeySchema(key_name="id", key_type=Key.HASH),
            # KeySchema(key_name="name", key_type=Key.RANGE),
        ]
    )
    table = Table(table_name="Humans", rcu=1, wcu=1)
    table.add_attribute(attribute_name="name", attribute_type="S", key_type="RANGE")
    table.add_attribute(attribute_name="id", attribute_type="N", key_type="HASH")

    print(table.dict())

    # new_table = Table(table_name="Humans", rcu=1, wcu=1)
    # new_table.add_attribute(attribute_name="name", attribute_type="S", key_type="RANGE")
    # print(new_table.dict())
