from OrderedSet import Node
from ..helpers.initiator import generate_unique_client_id

class Client(Node):
    def __init__(self, order_number=0, priority=0):
        # Inherit parents methods and properties
        super().__init__()

        # Create own preporties
        self.__id = generate_unique_client_id()
        self.__order_number = order_number
        self.__priority = priority

    def get_id(self):
        return self.__id

    def get_order_number(self):
        return self.__order_number
    
    def set_order_number(self, order_number):
        self.__order_number = order_number
    
    def get_priority(self):
        return self.__priority
    
    def set_priority(self, priority):
        self.__priority = priority

    def __eq__(self, other):
        return other and self.__id == other.__id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__id)
    
    def __repr__(self):
        return "<Client %s>" % (self.__id)

    def __str__(self):
        return "#%s %s (%s)" % (self.__order_number, self.__id, self.__priority)