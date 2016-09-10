"""
Given an array of integers, find if the array contains any duplicates.
Your function should return true if any value appears at least twice in the array, and it should return false if every element is distinct.

Subscribe to see which companies asked this question
"""

# instead of implement  a hash function, we can use the  built in function
class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        table=dict()
        for num in nums :
            if table.has_key(num): return  True
            table[num]=1

        return False