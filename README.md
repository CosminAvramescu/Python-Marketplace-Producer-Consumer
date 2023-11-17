![topology](https://i.imgur.com/qy7xIaf.png)
---producer.py After initialization from the constructor, when the thread is started, it enters the run method. Here we register the producer (thread), which gets an id. In an infinite loop, for each product in the producer's list, we add to its available_products list the amount of products offered. If its product queue is full, it waits with sleep. Otherwise, it waits after adding each product. If all consumers have called the place_order method, then all producers will be stopped.

---consumer.py In the run method, its created a new cart. For each add and remove operation in the consumer list, we add/remove the desired quantity from the cart. We wait with sleep while the product we want to add is not available in available_products. We call the place_order method and display each product in the cart.

---marketplace.py In the constructor we initialize the variables, the lock to allow a single thread to enter a critical area and the logging file. In register_producers, we increment the number of producers, which we also return as a string because this is the id of each producer. I used 2 dictionaries in the implementation (one that has the key producer_id and the value of the number of products added by the producer - to compare with the maximum queue length), (and the second dictionary has the key product and the value of the id of the producer who produced it - to quickly find if there is still a product object available in the marketplace). In publish, if the producer hasn't added any more products to available_products_by_type, then we initialize its dictionary entry. Same for no_of_products_by_producer. If no_of_products_per_producer[producer_id] is equal to the maximum of the queue, then we return False and the producer has to wait for the list to be released (basically for someone to consume products from it).Otherwise, add the producer id in the dictionary to the product key. In new_cart it is the same mechanism as in register_producer, we increment and return the id. In add_to_cart, we check if there is product in the dictionary, then add to the consumer's cart, subtract the number of available products of the producer (first dictionary) and remove the producer id from the product key in the second dictionary. In remove_from_cart, we remove the product from the cart and put it back in available products to be purchased by other consumers. In place_order, if there is no more item 0 in the list of consumers (all have called place_order), then we also stop the producer. We return the list of products in the cart. At TestMarketplace, we instantiate in setUp a marketplace, then test each method in the Marketplace class.