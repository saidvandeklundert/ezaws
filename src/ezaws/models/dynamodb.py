from pydantic import BaseModel
from enum import Enum

from typing import Union, Optional, List


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
    attributes: Attributes
    keys: Keys
    rcu: int  # ReadCapacityUnits: 1 is free
    wcu: int  # WriteCapacityUnits: 1 is free


"""
Delete response:
{'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                      'content-length': '317',
                                      'content-type': 'application/x-amz-json-1.0',
                                      'date': 'Sat, 28 May 2022 04:33:53 GMT',
                                      'server': 'Server',
                                      'x-amz-crc32': '3414060859',
                                      'x-amzn-requestid': '3FGB2S6JHUAR73MLARF6UIKTNFVV4KQNSO5AEMVJF66Q9ASUAAJG'},
                      'HTTPStatusCode': 200,
                      'RequestId': '3FGB2S6JHUAR73MLARF6UIKTNFVV4KQNSO5AEMVJF66Q9ASUAAJG',
                      'RetryAttempts': 0},
 'TableDescription': {'ItemCount': 0,
                      'ProvisionedThroughput': {'NumberOfDecreasesToday': 0,
                                                'ReadCapacityUnits': 1,
                                                'WriteCapacityUnits': 1},
                      'TableArn': 'arn:aws:dynamodb:eu-central-1:717687450252:table/Humans',
                      'TableId': 'a9149586-aae8-46c4-a07e-d8444a1cc466',
                      'TableName': 'Humans',
                      'TableSizeBytes': 0,
                      'TableStatus': 'DELETING'}}
"""

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
            KeySchema(key_name="name", key_type=Key.RANGE),
        ]
    )
    table = Table(table_name="Humans", attributes=attributes, keys=keys, rcu=1, wcu=1)
