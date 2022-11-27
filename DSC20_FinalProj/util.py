"""
DSC 20 Final Project Utility File

Please copy and paste your Stack and Queue implementation from Lab 10.
"""


class Collection:
    """
    A class to abstract the common functionalities of Stack and Queue.
    This class should not be initialized directly.
    """
    def __init__(self):
        """ Constructor. """
        # YOUR CODE GOES HERE #
        self.items = []
        self.num_items = 0

    def size(self):
        """ Get the number of items stored. """
        # YOUR CODE GOES HERE #
        return self.num_items 

    def is_empty(self):
        """ Check whether the collection is empty. """
        return self.num_items == 0

    def clear(self):
        """ Remove all items in the collection. """
        self.items = []
        self.num_items = 0


class Stack(Collection):
    """
    Stack class.
    """
    def push(self, item):
        """ Push `item` to the stack. """
        if item == None:
            raise ValueError('item cannot be None')
        self.items.append(item)
        self.num_items += 1
    def pop(self):
        """ Pop the top item from the stack. """
        # YOUR CODE GOES HERE #
        if self.is_empty():
            return None
        self.num_items -= 1
        return self.items.pop()

    def peek(self):
        """ Peek the top item. """
        # YOUR CODE GOES HERE #
        if self.is_empty():
            return None
        return self.items[self.size()-1]

    def __str__(self):
        """ Return the string representation of the stack. """
        # YOUR CODE GOES HERE #
        if self.is_empty():
            return "{0} {1}".format("(bottom)","(top)")
        string = ""
        for i in self.items:
            string += str(i) + " -- " 
        return "{0} {1}{2}".format("(bottom)", string[:-3], "(top)")


class Queue(Collection):
    """
    Queue class.
    """
    front_pointer = 0
    def enqueue(self, item):
        """ Enqueue `item` to the queue. """
        # YOUR CODE GOES HERE #
        if item == None:
            raise ValueError('item cannot be None')
        self.items.append(item)
        self.num_items += 1

    def dequeue(self):
        """ Dequeue the front item from the queue. """
        # YOUR CODE GOES HERE #
        if self.is_empty():
            return None
        removed = self.items[self.front_pointer]
        self.num_items -= 1
        self.front_pointer += 1
        return removed

    def peek(self):
        """ Peek the front item. """
        # YOUR CODE GOES HERE #
        if self.is_empty():
            return None
        return self.items[self.front_pointer]

    def __str__(self):
        """ Return the string representation of the queue. """
        # YOUR CODE GOES HERE #
        if self.is_empty():
            return "{0} {1}".format("(front)","(rear)")
        string = ""
        for i in self.items:
            string += str(i) + " -- " 
        return "{0} {1}{2}".format("(front)", string[:-3], "(rear)")

        
