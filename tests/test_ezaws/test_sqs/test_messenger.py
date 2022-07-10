from ezaws import Messenger
from ezaws.models.sqs import QueueAttributes, PurgeQueueResponse
from ezaws.sqs.functions import list_queues
from uuid import uuid4


QUEUE_NAME = str(uuid4()) + "_testing_queue_do_not_delete"
REGION = "eu-central-1"


def test_messenger_instantiation_from_name():
    msgnr = Messenger.from_queue_name(queue_name=QUEUE_NAME, region=REGION)
    assert isinstance(msgnr, Messenger)
    print(QUEUE_NAME, REGION)
    resp = msgnr._get_queue_url(queue_name=QUEUE_NAME, region_name=REGION)
    assert isinstance(resp, str)
    resp = msgnr.purge_queue()
    assert isinstance(resp, PurgeQueueResponse)
    msgnr.delete_queue()
    qs = list_queues(region=REGION)
    assert QUEUE_NAME not in qs.QueueUrls


def test_messenger_instantiation(test_q):
    msgnr = Messenger(
        queueu_url=test_q.url,
        region=test_q.region,
    )
    assert isinstance(msgnr, Messenger)


def test_send_messages(test_q):
    """Instantiate a messenger and send a message"""
    msgnr = Messenger(
        queueu_url=test_q.url,
        region=test_q.region,
    )
    msg_resp = msgnr.send_message(message="test_message")

    assert isinstance(msg_resp.MD5OfMessageBody, str)


def test_read_messages(test_q):
    """Instantiate a messenger and read a message"""
    msgnr = Messenger(
        queueu_url=test_q.url,
        region=test_q.region,
    )
    q_msgs = msgnr.read_messages(nr_of_messages=10)
    assert isinstance(q_msgs.Messages, list)


def test_delete_message(test_q):
    """Instantiate a messenger and read a message"""
    msgnr = Messenger(
        queueu_url=test_q.url,
        region=test_q.region,
    )
    msgnr.send_message(message="msg")
    q_msgs = msgnr.read_messages(nr_of_messages=10)
    while len(q_msgs.Messages) == 0:
        q_msgs = msgnr.read_messages(nr_of_messages=10)
    resp = msgnr.delete_message(receipt_handle=q_msgs.Messages[0]["ReceiptHandle"])
    assert resp.ResponseMetadata["HTTPStatusCode"] == 200


def test_get_queue_count(test_q):
    """Instantiate a messenger and read a message"""
    msgnr = Messenger(
        queueu_url=test_q.url,
        region=test_q.region,
    )
    q_msgs = msgnr.get_queue_count()

    assert isinstance(q_msgs, int)


def test_get_queue_attributes(test_q):
    msgnr = Messenger(
        queueu_url=test_q.url,
        region=test_q.region,
    )
    q_attr = msgnr.get_queue_attributes()
    assert isinstance(q_attr, QueueAttributes)
    assert q_attr.DelaySeconds == "0"
    assert q_attr.VisibilityTimeout == "30"
    assert "testing_queue_do_not_delete" in q_attr.QueueArn
