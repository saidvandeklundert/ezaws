import boto3
from dataclasses import dataclass
from ezaws.models.ssm import (
    GetParameterResponse,
    RegionParameters,
    CreateParameter,
    DeteleParameterResponse,
    CreateParameterResponse,
)


@dataclass
class ParameterStore:
    """
    Interface to the SSM Parameter store.
    """

    region: str

    def get_parameter(
        self, parameter: str, unencrypted: bool = True
    ) -> GetParameterResponse:
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

    def create_parameter(self, parameter: CreateParameter) -> CreateParameterResponse:
        """Create a parameter"""
        ssm_client = boto3.client("ssm", self.region)
        args = parameter.generate_parameter_args()

        client_response = ssm_client.put_parameter(**args)

        return CreateParameterResponse(**client_response)

    def delete_parameter(self, parameter_name: str) -> DeteleParameterResponse:
        """Delete a parameter from SSM parameter store."""
        ssm_client = boto3.client("ssm", self.region)
        arg = {"Name": parameter_name}
        client_response = ssm_client.delete_parameter(**arg)

        return DeteleParameterResponse(**client_response)
