import boto3
from dataclasses import dataclass
from ezaws.models.ssm import (
    GetParameterResponse,
    RegionParameters,
    Parameter,
    CreateParameter,
)


@dataclass
class ParameterStore:
    """
    Interface to the SSM Parameter store.

    TODO: create and delete parameter.
    """

    region: str

    def get_parameter(self, parameter: str, unencrypted: bool = True):
        """Retrieves target parameter, represented as a path to the parameter
        in SSM Parameter store."""
        ssm_client = boto3.client("ssm", self.region)

        client_response = ssm_client.get_parameter(
            Name=parameter, WithDecryption=unencrypted
        )

        return GetParameterResponse(**client_response)

    def describe_region_parameters(self) -> RegionParameters:
        """Returns information on a list of parameters in the region.
        Does not include the Value/secret itself."""
        ssm_client = boto3.client("ssm", self.region)

        client_response = ssm_client.describe_parameters()
        return RegionParameters(**client_response)

    def create_parameter(self, parameter: CreateParameter):
        """Create a parameter"""
        ssm_client = boto3.client("ssm", self.region)
        args = parameter.generate_parameter_args()

        client_response = ssm_client.put_parameter(**args)

        return client_response


"""
d = {
    "Version": 1,
    "Tier": "Standard",
    "ResponseMetadata": {
        "RequestId": "9d9e4546-b7fb-4a8c-acb2-576b7a95ae4a",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "server": "Server",
            "date": "Sun, 13 Mar 2022 20:37:56 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "31",
            "connection": "keep-alive",
            "x-amzn-requestid": "9d9e4546-b7fb-4a8c-acb2-576b7a95ae4a",
        },
        "RetryAttempts": 0,
    },
}
"""
