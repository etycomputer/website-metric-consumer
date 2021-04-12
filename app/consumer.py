import logging
from time import sleep
logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO, datefmt="%H:%M:%S")


class Consumer:
    log = None

    def __init__(self, log: logging):
        self.log = log

    def run(self, process_mode):
        try:
            while True:
                self.log.info('Consuming ' + process_mode)
                sleep(1)
        except KeyboardInterrupt:
            self.log.info("Exiting the background task.")


def create_consumer() -> Consumer:
    return Consumer(logging)
