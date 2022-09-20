from pydantic import BaseModel
import datetime
from ezaws.models.common import ResponseMetadata
from typing import List, Optional, Any

"""
response = client.put_parameter(
    Name='string',
    Description='string',
    Value='string',
    Type='String'|'StringList'|'SecureString',
    KeyId='string',
    Overwrite=True|False,
    AllowedPattern='string',
    Tags=[
        {
            'Key': 'string',
            'Value': 'string'
        },
    ],
    Tier='Standard'|'Advanced'|'Intelligent-Tiering',
    Policies='string',
    DataType='string'
)
"""


class CreateParameter(BaseModel):
    Name: str
    Description: Optional[str]
    Value: Optional[str]
    Type: str
    KeyId: Optional[str]
    Overwrite: bool = False
    Policies: Optional[List]
    Tier: Optional[str]
    AllowedPattern: Optional[str]

    def generate_parameter_args(self) -> dict:
        """Generate the Parameter arguments for use by removing all
        keys that have the value 'None'."""
        cur_d = vars(self)
        args = {}
        for key, value in cur_d.items():
            if value:
                args[key] = value
        return args


class Parameter(BaseModel):
    ARN: Optional[str]
    DataType: str
    LastModifiedDate: datetime.datetime
    LastModifiedUser: Optional[str]
    Name: str
    Type: str
    Value: Optional[str]
    Version: int
    Policies: Optional[List]
    Tier: Optional[str]
    AllowedPattern: Optional[str]
    Description: Optional[str]
    KeyId: Optional[str]


class GetParameterResponse(BaseModel):
    Parameter: Parameter
    ResponseMetadata: ResponseMetadata


class RegionParameters(BaseModel):
    Parameters: List[Parameter]
    ResponseMetadata: ResponseMetadata

    def __iter__(self) -> Any:
        return iter(self.Parameters)


class DeteleParameterResponse(BaseModel):
    ResponseMetadata: ResponseMetadata


class CreateParameterResponse(BaseModel):
    Version: int
    Tier: Optional[str]
    ResponseMetadata: ResponseMetadata
