"""
key thoughts
 1.merge sort
 2.two pointers
 3.recursion
 """

 # Definition for singly-linked list.
class ListNode(object):
     def __init__(self, x):
         self.val = x
         self.next = None


class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        return self.merge_sort(l1,l2)


    def merge_sort(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if l1 == None and l2==None: return None
        if l1 == None : return l2
        if l2 == None : return l1


        mergedList=ListNode(None)

        if  l1.val<l2.val:
            mergedList.val=l1.val
            l1=l1.next
            mergedList.next=self.merge_sort( l1, l2)
        else:
            mergedList.val = l2.val
            l2 = l2.next
            mergedList.next = self.merge_sort(l1, l2)



        return  mergedList


    def mergeTwoLists_twoPointers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        if  not l1  and not l2:
            return None


        head=ListNode(None)
        pointer=head

        while l1 and l2:
            if  l1.val<l2.val:
                pointer.next=l1
                l1=l1.next
            else:
                pointer.next = l2
                l2 = l2.next
            pointer=pointer.next

        if  l1:
                pointer.next=l1

        if  l2:
                pointer.next = l2


        return  head.next