# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


#use the dummy head to examine the all range
class Solution(object):
    def removeElements(self, head, val):
        """
        :type head: ListNode
        :type val: int
        :rtype: ListNode
        """

        dummyHead=ListNode(0)
        dummyHead.next=head

        current=dummyHead
        next=dummyHead.next

        while next :
            if  next.val == val:
                next=next.next
                current.next=next
            else:
                next=next.next
                current=current.next


        return  head

Node=ListNode(1)

s=Solution()
result=s.removeElements(Node,2)
print result