"""
138. Copy List with Random Pointer
 A linked list is given such that each node contains an additional random pointer which could point to any node in the list or null.

Return a deep copy of the list.
"""


#Definition for singly-linked list with a random pointer.
class RandomListNode(object):
    def __init__(self, x):
        self.label = x
        self.next = None
        self.random = None

class Solution(object):
    def copyRandomList(self, head):
        """
        :type head: RandomListNode
        :rtype: RandomListNode
        """
        if not head: return None
        relation = dict()

        # build relation
        cursor = head
        while cursor:
            relation[cursor] = RandomListNode(cursor.label)
            cursor = cursor.next


        cursor = head
        while cursor:

            if cursor.random:
                relation[cursor].random = relation[cursor.random]
            if cursor.next:
                relation[cursor].next = relation[cursor.next]

            cursor = cursor.next

        return relation[head]



if __name__ == "__main__":
    head   =   RandomListNode(1)
    sol = Solution()
    result = sol.copyRandomList(head)
    debug=1
