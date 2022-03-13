from pydantic import BaseModel
import datetime
from ezaws.models.common import ResponseMetadata
from typing import List, Optional


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
