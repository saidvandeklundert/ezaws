from typing import Dict, Optional, Union
from pydantic import BaseModel


class ResponseMetadata(BaseModel):
    RequestId: str
    HostId: Optional[str]
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, Union[str, bytes]]
    RetryAttempts: Optional[int]
