from ezaws.sqs.functions import list_queues
from uuid import uuid4
from ezaws import Messenger
from collections import namedtuple
import pytest

TestQ = namedtuple("TestQ", "url region")


@pytest.fixture(scope="session")
def test_q() -> TestQ:
    """returns a q name that can be used for testing"""

    region = "eu-central-1"
    qs = list_queues(region=region)
    for q_url in qs:
        if "_testing_queue_do_not_delete" in q_url:
            return TestQ(q_url, region)
    queue_name = str(uuid4()) + "_testing_queue_do_not_delete"
    msgnr = Messenger.from_queue_name(queue_name=queue_name, region=region)
    return TestQ(msgnr.queueu_url, region)
