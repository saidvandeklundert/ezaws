from ezaws import Lambda
from ezaws import Region
from ezaws.models.lambdas import ListFunctionsResponse


def test_list_functions():

    lambda_handler = Lambda(region=Region.eu_central_1)

    resp = lambda_handler.list_functions()
    assert isinstance(resp, ListFunctionsResponse)
