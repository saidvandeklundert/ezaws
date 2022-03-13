from ezaws.ssm.parameter_store import ParameterStore
from ezaws.models.ssm import CreateParameter
import datetime
from dateutil.tz import tzlocal

to_create = {
    "DataType": "text",
    "Name": "/passwords/infrastructure/created_parameter",
    "Type": "String",
    "Value": "SECRET_INFORMATION",
    "Version": 1,
    "Tier": "Standard",
    "Description": "Created with CreateParameter",
}
param_to_create = CreateParameter(**to_create)

if __name__ == "__main__":
    from pprint import pprint

    ps = ParameterStore(region="eu-central-1")
    param_resp = ps.get_parameter("/passwords/infrastructure/ssot_token")
    pprint(param_resp)
    region_param_resp = ps.describe_region_parameters()
    pprint(region_param_resp)

    for param in region_param_resp:
        pprint(param.Name)
    ps.create_parameter(parameter=param_to_create)
