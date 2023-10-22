"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread, Lock


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs
        self.lock = Lock()

    def run(self):
        # pentru fiecare operatie de add si remove din carts
        for i, _ in enumerate(self.carts):
            cart_id = self.marketplace.new_cart()
            for operation in self.carts[i]:
                if operation['type'] == 'add':
                    # adaugam cantitatea de produse dorite in marketplace.carts[cart_id]
                    quantity = operation['quantity']
                    while quantity != 0:
                        # asteptam cat timp nu e disponibil produsul in marketplace
                        while self.marketplace.add_to_cart(cart_id, operation['product']) is False:
                            time.sleep(self.retry_wait_time)
                        quantity -= 1
                elif operation['type'] == 'remove':
                    # eliminam cantitatea de produse din marketplace.carts[cart_id]
                    quantity = operation['quantity']
                    while quantity != 0:
                        self.marketplace.remove_from_cart(
                            cart_id, operation['product'])
                        quantity -= 1
            # dam comanda
            self.marketplace.print_lock.acquire()
            for i in self.marketplace.place_order(cart_id):
                print(f"{self.kwargs['name']} bought {i}")
            self.marketplace.print_lock.release()
