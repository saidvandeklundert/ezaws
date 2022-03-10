from ezaws import Messenger


def test_messenger_instantiation():
    msgnr = Messenger(
        queueu_url="https://eu-central-1.queue.amazonaws.com/717687450252/testing_queue_do_not_delete",
        region="eu-central-1",
    )
    assert isinstance(msgnr, Messenger)
