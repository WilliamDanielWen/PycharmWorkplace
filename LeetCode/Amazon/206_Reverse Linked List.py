"""
Reverse a singly linked list.
"""


#Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


# 1. use a stack
class Solution(object):
    def reverseList(self, head):
        """
        :type head: ListNode
        :rtype: ListNode

        """
        stack = []
        while head:
            stack.append(head.val)
            head=head.next

        head=ListNode(None)
        pointer=head
        for  i in range (len(stack)-1,-1,-1):
            pointer.next=ListNode(stack[i])
            pointer=pointer.next

        return head.next


#2. iterative solution
class Solution2(object):
    def reverseList(self, head):
        current=head
        reversedHead=None
        while current:
            temp=current.next

            #set current as the new head of the reversed list
            current.next=reversedHead

            #update the head of reversed list
            reversedHead=current

            current=temp

        return  reversedHead

