from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ResponseMetadata:
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: Optional[int]
