from ast import arg
from operator import inv
import boto3
import botocore
from ezaws import Region
from dataclasses import dataclass
from botocore.exceptions import ClientError
from ezaws.models.lambdas import ListFunctionsResponse, RunFunctionResponse
from typing import Union, Optional, Literal
import base64


@dataclass
class Lambda:
    """
    Interface to Lambda service.
    """

    region: Optional[Region] = None
    client: botocore.client = boto3.client("lambda")

    def __post_init__(self):
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

        args = {
            "FunctionName": function_name,
        }
        if invocation:
            args["InvocationType"] = invocation
        if log_type:
            args["LogType"] = log_type
        if payload:
            args["Payload "] = payload

        response = self.client.invoke(**args)
        response = RunFunctionResponse(**response)
        if response.LogResult:
            response.LogResult = base64.b64decode(response.LogResult)

        if response.ResponseMetadata.HTTPHeaders.get("x-amz-log-result"):
            response.ResponseMetadata.HTTPHeaders[
                "x-amz-log-result"
            ] = base64.b64decode(
                response.ResponseMetadata.HTTPHeaders["x-amz-log-result"]
            )

        return response


if __name__ == "__main__":
    from pprint import pprint

    # lambda_handler = Lambda(region=Region.eu_central_1)
    lambda_handler = Lambda()
    # resp = lambda_handler.list_functions()
    # pprint(resp)
    resp = lambda_handler.run_function(
        function_name="klundert-lambda-sam-helloworldpython3-E5pK6x3FSUfk",
        log_type=None,
    )
    pprint(resp.dict(), width=5)
    print(resp.LogResult)
