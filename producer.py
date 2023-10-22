"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

    def run(self):
        producer_id = self.marketplace.register_producer()

        while True:
            # pentru fiecare produs
            for i, _ in enumerate(self.products):
                # producem cantitatea de produs
                for _ in range(self.products[i][1]):
                    # asteptam cat timp este plina coada de produse
                    while self.marketplace.publish(producer_id, self.products[i][0]) is False:
                        if 0 not in self.marketplace.stop_event_consumer.values():
                            break
                        time.sleep(self.republish_wait_time)

                    time.sleep(self.products[i][2])
            # daca toti consumerii au apelat place_order
            if 0 not in self.marketplace.stop_event_consumer.values():
                break
