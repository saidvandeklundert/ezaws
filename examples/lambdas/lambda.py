from ezaws import Lambda


if __name__ == "__main__":
    from pprint import pprint

    # lambda_handler = Lambda(region=Region.eu_central_1)
    lambda_handler = Lambda()
    resp = lambda_handler.list_functions()
    pprint(resp)
    for func in resp:
        print(func.FunctionName)

    resp = lambda_handler.run_function(
        function_name="klundert-lambda-sam-helloworldpython3-E5pK6x3FSUfk",
        log_type=None,
    )
    pprint(resp.dict(), width=5)
    print(resp.LogResult)
    print(resp.payload_to_str())
