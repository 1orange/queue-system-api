class OrderedSet:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__size = 0

    def push(self, node) -> None:
        # If set is empty, assign head
        if not self.__head:
            self.__head = node
        
        # Relink tail
        self.__tail = self.link_tail(node)

        self.increment_size()

    def link_tail(self, node) -> None:
        """
        Link new node with tail node.
        Return None.
        """

        if self.__tail:
            self.__tail.set_next(node)
            node.set_prev(self.__tail)

            self.__tail = node
        
        return None

    def pop(self):
        return self.unlink_head()

    def unlink_head(self):
        """
        Unlink head tail with it's sibling.
        Assign new head tail and return unlinked one.
        """
        if self.__head:
            current_head = self.__head
            new_head = self.__head.get_next()

            # Unlink sibling nodes
            new_head.set_prev(None)
            current_head.set_next(None)

            self.__head = new_head
            return current_head
        
        return None

    def increment_size(self) -> None:
        self.__size += 1
    
    def get_size(self) -> int:
        return self.__size

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