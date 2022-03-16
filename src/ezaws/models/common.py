from typing import Dict, Optional
from pydantic import BaseModel


class ResponseMetadata(BaseModel):
    RequestId: str
    HostId: Optional[str]
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: Optional[int]
