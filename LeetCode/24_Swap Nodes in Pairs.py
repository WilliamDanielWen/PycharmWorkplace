# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        dummyHead= ListNode(0)
        dummyHead.next=head
        current=dummyHead
        while current.next!=None and current.next.next!=None:
            first=current.next
            second= current.next.next
            first.next=second.next
            second.next=first
            current.next=second
            current=current.next.next
        return dummyHead.next