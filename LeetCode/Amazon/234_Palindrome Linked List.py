"""
Given a singly linked list, determine if it is a palindrome.

Follow up:
Could you do it in O(n) time and O(1) space?

"""

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def isPalindrome(self, head):
        """
        :type head: ListNode
        :rtype:
        """
        if  head==None: return  True
        dummy=ListNode(0)
        dummy.next=head
        middle=dummy
        fast=dummy

        stack=[]
        while fast.next !=None and fast.next.next!=None:

            middle=middle.next
            stack.append(middle)
            fast=fast.next.next

        # odd number move the middle to the "middle", the middle element should be neglected
        if  fast.next!=None:
            middle=middle.next

        middle=middle.next
        while middle!=None:
            element=stack.pop()
            if element.val!=middle.val: return  False
            middle=middle.next

        return True

#there is another solution by reversing the firsvt half and by