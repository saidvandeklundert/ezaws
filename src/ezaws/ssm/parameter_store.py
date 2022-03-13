import boto3
from dataclasses import dataclass
from ezaws.models.ssm import GetParameterResponse, RegionParameters


@dataclass
class ParameterStore:
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


if __name__ == "__main__":
    from pprint import pprint

    ps = ParameterStore(region="eu-central-1")
    param_resp = ps.get_parameter("/passwords/infrastructure/ssot_token")
    pprint(param_resp)
    region_param_resp = ps.describe_region_parameters()
    pprint(region_param_resp)
