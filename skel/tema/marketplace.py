"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

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

        # date necesare producer: contor id_producer si dictionar pentru retinerea
        # (producator, produse fabricate):
        self.producer_id = -1
        self.producer_si_produse = {} # dict {producer_id: [produse]}

        # date necesare cart: contor id_cart si dictionar pentru retinerea
        # produselor adaugate:
        self.cart_id = -1
        self.cart_si_produse = {} # dict {cart_id: produs}

        # date necesare pentru rezervarea produselor:
        self.produse_disponibile = {} # dict {producer_id: lungime_lista_produse}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # obtin id-ul noului producer:
        self.producer_id = self.producer_id + 1

        # pentru noul id_producer generat initializez stochez in
        # dictionar cheia = producer_id si o lista nula pentru produse:
        self.producer_si_produse[str(self.producer_id)] = []
        # setez lungimea listei de produse disponibile a producerului curent:
        self.produse_disponibile.setdefault(str(self.producer_id), 0)

        # returnez id-ul producer-ului sub forma de string:
        return str(self.producer_id)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        # daca lungimea listei de produse ale producatorului curent este mai mica decat
        # queue_size_per_producer, mai adaug si produsul curent pentru a creste lungimea:
        if producer_id in self.producer_si_produse.keys():
            if len(self.producer_si_produse[producer_id]) < self.queue_size_per_producer:
                self.producer_si_produse[producer_id].append(product)
                # incrementez numarul de produse disponibile din marketplace
                self.produse_disponibile[producer_id] = self.produse_disponibile[producer_id] + 1

                return True

        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # obtin id-ul cart-ului curent:
        self.cart_id = self.cart_id + 1

        # pentru noul cart_id generat stochez in dictionar
        # cheia = cart_id si o lista nula pentru produse:
        self.cart_si_produse[self.cart_id] = []

        return self.cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        lista_id_uri_produceri = self.producer_si_produse.keys()
        # pentru fiecare producator:
        for prod_id in lista_id_uri_produceri:
            # daca produsul se afla in lista de produse ale producer-ului curent:
            if product in self.producer_si_produse[prod_id]:
                # adaug produsul in cart-ul curent:
                self.cart_si_produse[cart_id].append(product)
                # decrementez numarul de produse disponibile ale producer-ului curent:
                self.produse_disponibile[prod_id] = self.produse_disponibile[prod_id] - 1

                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        lista_id_uri_produceri = self.producer_si_produse.keys()
        # pentru fiecare producator:
        for prod_id in lista_id_uri_produceri:
            # daca produsul meu se afla in produsele din cart-ul actual:
            if product in self.cart_si_produse[cart_id]:
                # elimin produsul din cart-ul actual
                self.cart_si_produse[cart_id].remove(product)
                # incrementez numarul de produse disponibile ale producer-ului curent:
                self.produse_disponibile[prod_id] = self.produse_disponibile[prod_id] - 1

                break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # pentru fiecare produs din cartul curent:
        for produs in self.cart_si_produse[cart_id]:
            # tinand cont de producer_id si lungimea listei de produse a sa:
            for prod_id, produse_curente in self.producer_si_produse.items():
                # daca produsul din cart se afla in lista producer-ului curent:
                if produs in produse_curente:
                    # daca lungimea listei de produse disponibile este mai mica decat lungimea
                    # listei de produse a producer-ului curent:
                    if self.produse_disponibile[prod_id] < len(self.producer_si_produse[prod_id]):
                        # elimin produsul din lista de produse a producer-ului curent:
                        self.producer_si_produse[prod_id].remove(produs)

        # returnez lista de produse din cart-ul curent:
        return self.cart_si_produse[cart_id]
