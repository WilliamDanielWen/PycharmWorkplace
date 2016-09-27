# Definition for singly-linked list.

class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

# use the equal distance to the intersection point
class Solution(object):
    def getIntersectionNode(self, headA, headB):
        """
        :type head1, head1: ListNode
        :rtype: ListNode
        """

        pA=headA
        pB=headB

        if  pA==None or  pB==None :  return  None


        while True:
            if pA ==pB: return  pA   #intersection

            pA = pA.next
            pB = pB.next

            if  pA==None and pB==None : return None # intersection didn' t exist

            #one of them reach the end
            if pA == None: pA = headB
            if pB == None: pB = headA







NodeA=ListNode("1")
NodeB=ListNode("2")
NodeC=ListNode("3")

NodeA.next=NodeB
NodeB.next=NodeC


NodeD=ListNode("4")




s=Solution()
result=s.getIntersectionNode(NodeA,NodeD)

print  result.val
