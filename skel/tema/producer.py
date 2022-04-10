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
    producer_id: str

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
        # generez un id pentru producatorul curent:
        self.producer_id = self.marketplace.register_producer()
        
        # cat timp programul se executa parcurg produsele producatorului curent si incerc sa le public:
        while True:
            for current_product in self.products:
                cantitate_produsa = 0;
                cantitate_maxima_produse = current_product[1]  
                timp_producere = current_product[2]              

                # pana am atins cantitatea dorita din tipul produsului, incerc sa il public in marketplace:
                while (cantitate_produsa < cantitate_maxima_produse):
                   publicat = self.marketplace.publish(self.producer_id, current_product)
                    
                    # daca s-a putut publicat produsul cu succes, astept timpul necesar pentru producere
                    # si dupa trec la urmatoarea producere, iar daca operatia nu s-a efectuat cu succes
                    # din diverse motive, astept pana pot reincerca publicarea:
                    if publicat is True:
                        # timp necesar pentru producerea produsului actual:
                        time.sleep(timp_producere)

                        # trec la urmatoarea producere:
                        cantitate_produsa = cantitate_produsa + 1;
                    else:
                        time.sleep(self.republish_wait_time)
