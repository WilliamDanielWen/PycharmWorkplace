"""
Design and implement a data structure for Least Recently Used (LRU) cache. It should support the following operations: get and set.

get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
set(key, value) - Set or insert the value if the key is not already present. When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.


"""


class LRUCache(object):
    def __init__(self, capacity):
        """
        :type capacity: int
        """

    def get(self, key):
        """
        :rtype: int
        """

    def set(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: nothing

        """



        """
        if has key :   O(1)

            modify:
                set hash table value :O(1)



        else:
            check capacity: O(n)

            if capacity is full
                hash table deletion O(n)
                linked list deletion last O(1)

            insert a new element
                hash table insertion O(n)
                linked list insertion O(1)


        """





