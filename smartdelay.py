import random, time

random.seed()

def delay(basetime, divider):
    amount = abs(basetime + random.randint(-5, 5)/divider)
    time.sleep(amount)
