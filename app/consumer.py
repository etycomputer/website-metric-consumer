import logging
from time import sleep
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


class Consumer:
    def __init__(self, log: logging):
        self.log = log


def create_consumer() -> Consumer:
    return Consumer(logging)
