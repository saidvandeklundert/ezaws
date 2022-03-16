from ezaws.ssm.parameter_store import ParameterStore
from ezaws.models.ssm import CreateParameter
import time

to_create = {
    "DataType": "text",
    "Name": "/passwords/infrastructure/created_parameter",
    "Type": "String",
    "Value": "SECRET_INFORMATION",
    "Version": 1,
    "Tier": "Standard",
    "Description": "Created with CreateParameter",
    "Overwrite": True,
}
param_to_create = CreateParameter(**to_create)

if __name__ == "__main__":
    from pprint import pprint

    ps = ParameterStore(region="eu-central-1")

    print("Creating parameter")
    ps.create_parameter(parameter=param_to_create)
    time.sleep(3)
    print("Retrieve parameter")
    param_resp = ps.get_parameter("/passwords/infrastructure/created_parameter")
    pprint(param_resp)
    print("Retrieve all parameters")
    region_param_resp = ps.describe_region_parameters()
    for param in region_param_resp:
        pprint(param.Name)

    print("Deleting parameter")
    ps.delete_parameter("/passwords/infrastructure/created_parameter")
    time.sleep(3)
    print("Retrieve all parameters")
    region_param_resp = ps.describe_region_parameters()
    for param in region_param_resp:
        pprint(param.Name)
