from ezaws import Messenger
from ezaws import Message
from pprint import pprint
from ezaws import Region

if __name__ == "__main__":

    # instantiate the messanger
    msgnr = Messenger.from_queue_name(
        queue_name="example-queue", region=Region.eu_central_1
    )

    # send a few messages
    msg = msgnr.send_message("message 1")
    msg = msgnr.send_message("message 2")
    msg = msgnr.send_message("message 3")
    msg = msgnr.send_message("message 4")
    msg = msgnr.send_message("message 5")
    pprint(msg)

    # read and delete messages:
    msg_read = msgnr.read_messages(nr_of_messages=10)

    for m in msg_read:
        m = Message(**m)
        print(f"read message {m.Body}")
        resp = msgnr.delete_message(receipt_handle=m.ReceiptHandle)
