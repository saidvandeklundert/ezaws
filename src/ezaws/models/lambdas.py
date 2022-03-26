from ezaws.models.common import ResponseMetadata
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class Function(BaseModel):
    Architectures: List[str]
    CodeSha256: str
    CodeSize: int
    Description: str
    Environment: Optional[Dict[str, Any]] = None
    FunctionArn: str
    FunctionName: str
    Handler: str
    LastModified: str
    MemorySize: int
    PackageType: str
    RevisionId: str
    Role: str
    Runtime: str
    Timeout: int
    TracingConfig: Dict[str, str]
    Version: str


class ListFunctionsResponse(BaseModel):
    Functions: List[Function]
    ResponseMetadata: ResponseMetadata


class RunFunctionResponse(BaseModel):
    ExecutedVersion: str
    LogResult: Optional[str] = None
    ResponseMetadata: ResponseMetadata
    StatusCode: int
    Payload: Any

    def payload_to_str(self) -> str:
        ret_str = ""
        for some_bytes in self.Payload:
            ret_str += some_bytes.decode("utf-8")
        return ret_str
