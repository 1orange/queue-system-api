from typing import Iterable
from .OrderedSet import OrderedSet

class Queue:
    def __init__(self, logger):
        self.__queue = OrderedSet(logger)
        self.__latest_order_number = 1
        self.__queue_size = 0
        self.__logger = logger

    def enqueue(self, client):
        """
        Add client in to the queue.
        Return client's order number
        """
        # Get current order number
        current_order_number = self.get_order_number()
        
        # Set clients order number
        client.set_order_number(current_order_number)

        # Enqueue client
        self.__queue.push(client)
        
        # Increment order number
        self.increment_order_number()

        # Increment queue size
        self.increment_queue_size()
        
        return client

    def dequeue(self):
        """
        Pop client from queue.
        Return client's order number.
        """
        # Check whether queue is not empty
        if not self.__queue:
            return None

        # Get first client to go
        current_client = self.__queue.pop()

        # Decrement queue size
        self.decrement_queue_size()

        # Sort remaining clients
        self.__sort_queue()
        
        return current_client.get_order_number()

    def __sort_queue(self):
        # TODO: Sort based on client's priority
        pass

    def get_iterable(self):
        return self.__queue.get_iterable()
    
    def preview(self):
        self.__logger.info(f"Current queue ({self.get_size()}):")
        
        self.__queue.print()


    def get_order_number(self):
        return self.__latest_order_number


    def increment_order_number(self):
        self.__latest_order_number += 1


    def increment_queue_size(self):
        self.__queue_size += 1


    def decrement_queue_size(self):
        self.__queue_size -= 1


    def get_size(self):
        return self.__queue_size
