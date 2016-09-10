# Definition for singly-linked list.

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

#use two pointers
class Solution(object):
    def deleteDuplicates(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """

        current=head

        while  current :
                probe = current.next
                if probe == None: break
                while probe.val==current.val: #find the next qulified element
                        probe=probe.next
                        if  probe==None: break

                current.next=probe #skip the duplicate if it exists

                current = current.next #continue to examine the next

        return head

#how to solve it recursively?

