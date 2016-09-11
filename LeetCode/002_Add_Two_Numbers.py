"""
You are given two linked lists representing two non-negative numbers.
The digits are stored in reverse order and each of their nodes contain a single digit.
Add the two numbers and return it as a linked list.

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8


"""


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None



class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """

        #creat dummy head dealing with when l1 l2 are both empty
        dummy_head=ListNode(0)

        cursor=dummy_head

        digit_sum = 0
        while l1!=None or l2!=None:

            if l1 !=None:
                digit_sum +=l1.val
                l1=l1.next

            if l2 !=None:
                digit_sum +=l2.val
                l2=l2.next

            value =digit_sum%10
            cursor.next=ListNode(value)
            cursor=cursor.next

            #check if there is carry bit
            digit_sum /= 10

        # there is carry bit at the time when traverse is over
        if digit_sum==1:
            cursor.next = ListNode(1)
            cursor = cursor.next

        return dummy_head.next


if __name__=="__main__":
    s=Solution()

    # l1=ListNode(2)
    # l1.next=ListNode(4)
    # l1.next.next=ListNode(3)
    #
    # l2=ListNode(5)
    # l2.next=ListNode(6)
    # l2.next.next=ListNode(4)


    l1=ListNode(5)


    l2=ListNode(5)



    result=s.addTwoNumbers(l1,l2)
    while result!=None:
        print result.val
        result=result.next