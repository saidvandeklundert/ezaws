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
    pprint(vars(msgnr.get_queue_attributes()))

    """
    print(msgnr.get_queue_count())
    print(msgnr.get_queue_attributes())


    msg = msgnr.send_message("message 3")
    msg = msgnr.send_message("message 4")
    msg = msgnr.send_message("message 5")

    msg_read = msgnr.read_messages(nr_of_messages=10)

    for m in msg_read:
        m = Message(**m)
        print(f"read message {m.Body}")
        msgnr.delete_message(receipt_handle=m.ReceiptHandle)


    """
    """

for m in msg_read:
    m = Message(**m)
    print(f"read message {m.Body}")
    msgnr.delete_message(receipt_handle=m.ReceiptHandle)
    """
    """
    qs = list_queues(region="eu-central-1")
    pprint(qs)

    
    for q in qs.QueueUrls:
        print(q)
        if "testing_queue_do_not_delete" in q:
            delete_queue(queue_name=q, region="eu-central-1")
    pprint(list_queues(region="eu-central-1"))
    
    queue_name = "example-queue"
    create_queue_resp = create_queue(queue_name)
    pprint(create_queue_resp)
    queue_url_resp = get_queue_url(queue_name)
    print("get queue response")
    pprint(queue_url_resp)
    val = input("Type 'delete' in case you want to delete the 'example-queue':")
    if val == "delete":
        delete_queu_response = delete_queue(queue_name)
        print("delete queue response")
        pprint(delete_queu_response)
    else:
        print("'example-queue' is not deleted.")
    queueu_url = "https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"
    region_name = "eu-central-1"

    print("Purging queue:")
    pugre_response = purge_queue(queueu_url=queueu_url, region_name=region_name)
    pprint(pugre_response)
    queueu_url = "https://eu-central-1.queue.amazonaws.com/717687450252/example-queue"
    region_name = "eu-central-1"
    print("sending message:")
    send_response = send_message(
        queueu_url=queueu_url,
        region_name=region_name,
        message='{"important-key":"important-value-1"}',
    )
    pprint(send_response)
    time.sleep(2)
    receive_response = receive_message(
        queueu_url=queueu_url, region_name=region_name, nr_of_messages=10
    )

    send_message_id = send_response["MessageId"]
    send_message_md5 = send_response["MD5OfMessageBody"]
    print(
        f"\n\n\nMessage that was send to the queue has id {send_message_id} and md5 {send_message_md5}.\n\n"
    )

    to_delete = []
    print("Messages in the queue:")
    for msg in receive_response["Messages"]:
        pprint(msg)
        to_delete.append(msg["ReceiptHandle"])
    print(f"Deleting messages with the following receipt handles:")
    for item in to_delete:
        print(item)
    for receipt_handle in to_delete:

        delete_response = delete_message(
            queueu_url=queueu_url,
            region_name=region_name,
            receipt_handle=receipt_handle,
        )
        pprint(delete_response)
    """
