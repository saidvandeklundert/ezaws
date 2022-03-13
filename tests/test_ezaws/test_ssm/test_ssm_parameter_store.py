from ezaws import ParameterStore
from ezaws.models.ssm import GetParameterResponse, RegionParameters

"""
    ps = ParameterStore(region="eu-central-1")
    param_resp = ps.get_parameter("/passwords/infrastructure/ssot_token")
    pprint(param_resp)
    region_param_resp = ps.get_region_parameters()
    pprint(region_param_resp)
"""


def test_get_parameter():
    ps = ParameterStore(region="eu-central-1")
    param_resp = ps.get_parameter("/passwords/infrastructure/ssot_token")
    assert isinstance(param_resp, GetParameterResponse)


def test_describe_region_parameters():
    ps = ParameterStore(region="eu-central-1")
    region_param = ps.describe_region_parameters()
    assert isinstance(region_param, RegionParameters)
