def producer():
    for item in ["a", "b", "c"]:
        print("producer: made", item)
        yield item              # pause here, hand control back

def consumer():
    for item in producer():     # resume the producer each time
        print("consumer: used", item)

consumer()
