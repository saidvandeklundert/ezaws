from ezaws import Messenger
from pprint import pprint
from ezaws import Region

if __name__ == "__main__":

    msgnr = Messenger.from_queue_name(
        queue_name="example-queue", region=Region.eu_central_1
    )

    msg = msgnr.send_message("message 1")

    pprint(msg)
    q_count = msgnr.get_queue_count()
    print(q_count)
