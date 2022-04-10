"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

class Consumer(Thread):
    """
    Class that represents a consumer.
    """
    cart_id: int
    actiuni = ["add", "remove"]

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
        pass

    def run(self):
        # parcurg cart-ul curent din toate cart-urile disponibile:
        for current_cart in self.carts:
            # generez un id pentru cart-ul curent
            self.cart_id = self.marketplace.new_cart()

            # parcurg actiunile disponibile pentru cart-ul curent:
            for actiune_cart in current_cart:
                # verific daca este o actiuene de adaugare sau de eliminare:
                if actiune_cart['type'].startswith('a'):
                    cantitate_adaugata = 0
 
                    # adaug produse pana cand ating limita maxima: 
                    while (cantitate_adaugata < actiune_cart['quantity']):
                        # incerc sa adaug produsul in cart:
                        adaugat = self.marketplace.add_to_cart(self.cart_id, actiune_cart['product'])
                        
                        # daca s-a adaugat produsul in cart, trec la urmatoarea adaugare,
                        # iar daca operatia a esuat, astept timpul necesar pentru reincercare:
                        if adaugat is True:
                            cantitate_adaugata = cantitate_adaugata + 1
                        else:
                            time.sleep(self.retry_wait_time)

                if actiune_cart['type'].startswith('r'):
                    cantitate_eliminata = 0
                    
                    # elimin produse pana ating limita maxima:
                    while (cantitate_eliminata < actiune_cart['quantity']):
                        # incerc sa elimin produsul din cart:
                        eliminat = self.marketplace.remove_from_cart(self.cart_id, actiune_cart['product'])
                        
                        # daca s-a eliminat produsul din cart, trec la urmatoarea eliminare,
                        # iar daca operatia a esuat, astept timpul necesar pentru reincercare:
                        if eliminat is True:
                            cantitate_eliminata = cantitate_eliminata + 1
                        else:
                            time.sleep(self.retry_wait_time)
