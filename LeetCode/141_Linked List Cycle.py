"""
walker can't catch up runner before runner  encountered  the cycle
let
    waker walks k steps, encountered cycle i times
    runner runs 2k steps, encountered cycle j times
    every cycle  reduce r steps
so, j>i

we only need to prove that 2k-j*r=k-i*r always holds true:
    so k=(j-i)r
    since j>i and is integer, r is also positive integer, (j-i)r is also positive integer
    so k=(j-i)r can always holds true
"""


# Definition for singly-linked list.
class ListNode(object):
     def __init__(self, x):
         self.val = x
         self.next = None

class Solution(object):
    def hasCycle(self, head):
        """
        :type head: ListNode
        :rtype: bool
        """
        if  head==None: return  False
        runner=head
        walker=head
        while runner.next!=None and  runner.next.next!=None:
            runner=runner.next.next
            walker=walker.next
            if runner==walker: return True

        return False