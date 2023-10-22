"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock
import unittest
import logging
from logging.handlers import RotatingFileHandler


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.carts = []
        self.producers = -1
        self.carts_number = -1
        self.no_of_products_per_producer = {}
        self.lock_producer = Lock()
        self.lock_consumer = Lock()
        self.stop_event_consumer = {}
        self.available_products_by_type = {}
        self.print_lock = Lock()

        # setam fisierul de logging
        self.log = logging.getLogger()
        self.log.setLevel('WARNING')
        rotating_file_handler = RotatingFileHandler('marketplace.log', mode='a',
                                                    maxBytes=10000000,
                                                    backupCount=6, encoding=None, delay=True)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        rotating_file_handler.setFormatter(formatter)
        self.log.addHandler(rotating_file_handler)

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.log.info("Enter register_producer")
        self.lock_producer.acquire()
        # incrementam numarul de producers si returnam id-ul
        self.producers += 1
        self.lock_producer.release()
        self.log.info("Exit register_producer")
        return str(self.producers)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        self.log.info("Enter publish(%s, %s)", producer_id, product)
        # daca nu a mai produs nimic producerul
        if producer_id not in self.no_of_products_per_producer:
            self.no_of_products_per_producer[producer_id] = 0

        # daca e coada de produse plina
        if self.no_of_products_per_producer[producer_id] == self.queue_size_per_producer:
            return False

        # daca nu a mai fost adaugat nimic la cheia product
        if product not in self.available_products_by_type:
            self.available_products_by_type[product] = []

        # adaugam id-ul producerului la cheia product
        self.available_products_by_type[product].append(producer_id)
        self.lock_producer.acquire()
        self.no_of_products_per_producer[producer_id] += 1
        self.lock_producer.release()
        self.log.info("Exit publish")

        return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.log.info("Enter new_cart")
        # adaugam cart-ul la lista de liste
        self.carts.append([])
        self.lock_consumer.acquire()
        # incrementam si setam id-ul cart-ului
        self.carts_number += 1
        cart_id = self.carts_number
        self.lock_consumer.release()
        self.stop_event_consumer[cart_id] = 0
        self.log.info("Exit new_cart")
        return cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        self.log.info("Enter publish(%d, %s)", cart_id, product)

        # exista tipul de produs disponibil
        if product in self.available_products_by_type and \
                self.available_products_by_type[product] != []:
            # adaugam in cart produsul
            self.carts[cart_id].append(product)
            key = self.available_products_by_type[product][0]
            # scadem numarul de produse ale producerului
            self.no_of_products_per_producer[key] -= 1
            # eliminam produsul din available_products
            self.available_products_by_type[product].pop(0)
            return True

        self.log.info("Exit add_to_cart")
        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.log.info("Enter publish(%d, %s)", cart_id, product)
        self.carts[cart_id].remove(product)
        # eliminam din cart produsul si il punem inapoi in available_products
        if '0' not in self.no_of_products_per_producer:
            self.no_of_products_per_producer['0'] = 1
        else:
            self.available_products_by_type[product].append('0')
            self.lock_consumer.acquire()
            self.no_of_products_per_producer['0'] += 1
            self.lock_consumer.release()

        self.log.info("Exit add_to_cart")

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.log.info("Enter place_order %d", cart_id)
        self.stop_event_consumer[cart_id] = 1

        self.log.info("Exit place_order")
        return self.carts[cart_id]


class TestMarketplace(unittest.TestCase):
    def setUp(self):
        """
        setUp
        """
        self.marketplace = Marketplace(15)

    def test_register_producer(self):
        """
        test_register_producer
        """
        self.assertEqual(1 + int(self.marketplace.register_producer()),
                         int(self.marketplace.register_producer()))

    def test_new_cart(self):
        """
        test_new_cart
        """
        self.assertEqual(self.marketplace.new_cart(), 0)
        self.assertEqual(self.marketplace.new_cart(), 1)
        self.assertEqual(len(self.marketplace.carts), 2)

    def test_publish(self):
        """
        test_publish
        """
        # inregistram producator si adaugam produse
        producer_id = self.marketplace.register_producer()
        tea = 'Tea(name="Linden", price=10, type="Herbal")'
        coffee = 'Coffee(name="Indonezia", price=5, acidity=5.05, roast_level="MEDIUM")'
        self.marketplace.publish(producer_id, tea)
        self.marketplace.publish(producer_id, coffee)
        self.assertEqual(self.marketplace.available_products_by_type[tea],
                         [producer_id])
        self.assertEqual(self.marketplace.available_products_by_type[coffee],
                         [producer_id])

    def test_add_to_cart(self):
        """
        test_add_to_cart
        """
        # inregistram producator, adaugam produse si cream cart
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        tea = 'Tea(name="Linden", price=10, type="Herbal")'
        coffee = 'Coffee(name="Indonezia", price=5, acidity=5.05, roast_level="MEDIUM")'

        self.marketplace.publish(producer_id, tea)
        self.marketplace.publish(producer_id, coffee)
        self.marketplace.add_to_cart(cart_id, tea)
        self.marketplace.add_to_cart(cart_id, coffee)

        # verificam ca s-au adaugat corect produsele in cart
        self.assertEqual(self.marketplace.carts[cart_id], [tea, coffee])
        self.assertEqual(
            self.marketplace.no_of_products_per_producer[producer_id], 0)

    def test_remove_from_cart(self):
        """
        test_remove_from_cart
        """
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        tea = 'Tea(name="Linden", price=10, type="Herbal")'
        coffee = 'Coffee(name="Indonezia", price=5, acidity=5.05, roast_level="MEDIUM")'
        self.marketplace.publish(producer_id, tea)
        self.marketplace.publish(producer_id, coffee)
        self.marketplace.add_to_cart(cart_id, tea)
        self.marketplace.add_to_cart(cart_id, coffee)

        # dupa adaugarea produselor, stergem unul
        self.marketplace.remove_from_cart(cart_id, tea)
        # verificam ca a ramas produsul corect in cart
        self.assertEqual(self.marketplace.carts[cart_id], [coffee])
        self.assertEqual(
            self.marketplace.no_of_products_per_producer[producer_id], 1)

    def test_place_order(self):
        """
        place_order
        """
        cart_id = self.marketplace.new_cart()
        producer_id = self.marketplace.register_producer()
        tea = 'Tea(name="Linden", price=10, type="Herbal")'
        coffee = 'Coffee(name="Indonezia", price=5, acidity=5.05, roast_level="MEDIUM")'
        self.marketplace.publish(producer_id, tea)
        self.marketplace.publish(producer_id, coffee)
        self.marketplace.add_to_cart(cart_id, tea)
        self.marketplace.add_to_cart(cart_id, coffee)
        self.assertEqual(self.marketplace.place_order(cart_id), [tea, coffee])
