"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""


from re import M
import time

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
        self.cart_si_produse = {} # dict {cart_id: [produse]}
        
        # date necesare pentru rezervarea produselor:
        self.produse_disponibile = [] # [[produs, producer_id]]
        self.producer_ids_rezervate = {} #dict {producer_id: [produs, cart_id]}

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        # obtin id-ul noului producer: 
        self.producer_id = self.producer_id + 1
        
        # pentru noul id_producer generat initializez stochez in
        # dictionar cheia = producer_id si o lista nula pentru produse:
        self.producer_si_produse[str(self.producer_id)] = []

        # print(self.producer_id)
        # returnez id-ul producer-ului sub forma de string:
        a = self.producer_id
        return str(a)

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
                self.produse_disponibile.append([product, producer_id])
                # print('inainte true')
                return True  

        # print('inainte false')
        return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        # obtin id-ul cart-ului curent:
        self.cart_id = self.cart_id + 1
        
        # pentru noul cart_id generat stochez in 
        # dictionar cheia = cart_id si o lista nula pentru produse: 
        self.cart_si_produse[self.cart_id] = []
        # print(self.cart_id)
        # returnez id-ul cart-ului:
        # print("PRODUCATORUL ARE LA INITIEREA CARTULUI")
        # print(self.producer_si_produse)
        # print(self.produse_disponibile)
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
        # parcurg elementele disponibile la momentul actual din partea
        # tuturor producerilor:
        for cheie in self.producer_si_produse.keys():
            for lista in self.produse_disponibile:
                if (lista[0] == product) and (lista[1] == cheie):
                    # daca produsul exista in lista de produse disponibile,
                    # il adaug in lista de produse din cart:
                    self.produse_disponibile.remove(lista)
                    self.producer_ids_rezervate.update({cheie: [product, cart_id]})
                    self.cart_si_produse[cart_id].append(product)
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
        # daca produsul meu se afla in produsele din cart-ul actual:
        if product in self.cart_si_produse[cart_id]:
            # elimin produsul din cart-ul actual
            self.cart_si_produse[cart_id].remove(product)

            # adaug produsul inapoi in produsele disponibile in marketplace
            for cheie in self.producer_ids_rezervate.keys():
                if (self.producer_ids_rezervate[cheie][1] == cart_id):
                    self.produse_disponibile.append([self.producer_ids_rezervate[cheie][0], cheie])

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        # print("lungime")
        # print(len(self.producer_si_produse["0"]))
        # print("PRODUCATORUL ARE INAINTE DE CUMPARARE")
        # print(self.producer_si_produse)
        # print(self.produse_disponibile)
        
        for produs in self.cart_si_produse[cart_id]:
            for cheie in self.producer_ids_rezervate.keys():
                if (self.producer_ids_rezervate[cheie][1] == cart_id):
                    self.producer_si_produse[cheie].remove(produs)            
            
        return self.cart_si_produse[cart_id]
