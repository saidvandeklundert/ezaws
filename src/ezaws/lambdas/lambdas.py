import boto3
import botocore
from ezaws import Region
from dataclasses import dataclass
from ezaws.models.lambdas import ListFunctionsResponse, RunFunctionResponse
from typing import Union, Optional, Literal, Any
import base64


@dataclass
class Lambda:
    """
    Interface to Lambda service.
    """

    region: Optional[Region] = None
    client: botocore.client = boto3.client("lambda")

    def __post_init__(self) -> None:
        if self.region:
            self.client = boto3.client("lambda", region_name=self.region)

    def list_functions(self) -> ListFunctionsResponse:
        """List all functions for a region."""
        response = self.client.list_functions()
        return ListFunctionsResponse(**response)

    def run_function(
        self,
        function_name: str,
        payload: Optional[Union[str, bytes]] = None,
        invocation: Optional[Literal["RequestResponse", "Event", "DryRun"]] = None,
        log_type: Optional[Literal["Tail"]] = "Tail",
    ) -> RunFunctionResponse:

        args: dict[Any, Any] = {
            "FunctionName": function_name,
        }
        if invocation:
            args["InvocationType"] = invocation
        if log_type:
            args["LogType"] = log_type
        if payload:
            args["Payload "] = payload

        response = self.client.invoke(**args)
        func_response = RunFunctionResponse(**response)
        if func_response.LogResult:
            func_response.LogResult = base64.b64decode(response.LogResult)

        if func_response.ResponseMetadata.HTTPHeaders.get("x-amz-log-result"):
            func_response.ResponseMetadata.HTTPHeaders[
                "x-amz-log-result"
            ] = base64.b64decode(
                func_response.ResponseMetadata.HTTPHeaders["x-amz-log-result"]
            )

        return func_response
