import random, time

random.seed()

def delay(basetime, divider):
    amount = abs(basetime + random.randint(-5, 5)/divider)
    # print("Sleeping %ss" % str(amount))
    time.sleep(amount)
