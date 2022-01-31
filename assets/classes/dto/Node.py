class Node():
    def __init__(self):
        self.__prev = None
        self.__next = None

    def set_prev(self, prev_node):
        self.__prev = prev_node

    def get_prev(self):
        return self.__prev

    def set_next(self, next_node):
        self.__next = next_node

    def get_next(self):
        return self.__next
