from ezaws.models.dynamodb import Table, GetItemResponse


def test_table_creation():
    table = Table(table_name="Humans", rcu=1, wcu=1)
    table.add_attribute(attribute_name="name", attribute_type="S", key_type="RANGE")
    table.add_attribute(attribute_name="id", attribute_type="N", key_type="HASH")
    assert isinstance(table, Table)


def test_GetItemResponse():
    get_item_response = GetItemResponse(
        **{
            "Item": {"id": "1828", "name": "Arnetta"},
            "ResponseMetadata": {
                "HTTPHeaders": {
                    "connection": "keep-alive",
                    "content-length": "51",
                    "content-type": "application/x-amz-json-1.0",
                    "date": "Tue, 31 May 2022 06:43:40 GMT",
                    "server": "Server",
                    "x-amz-crc32": "859391921",
                    "x-amzn-requestid": "KNCSVK20TCKSJSVFJQQTCVR647VV4KQNSO5AEMVJF66Q9ASUAAJG",
                },
                "HTTPStatusCode": 200,
                "RequestId": "KNCSVK20TCKSJSVFJQQTCVR647VV4KQNSO5AEMVJF66Q9ASUAAJG",
                "RetryAttempts": 0,
            },
        }
    )
    assert get_item_response
