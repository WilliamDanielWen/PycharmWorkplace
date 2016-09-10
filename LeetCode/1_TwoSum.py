'''
Given an array of integers, return indices of the two numbers such that they add up to a specific target.

You may assume that each input would have exactly one solution.

Example:
Given nums = [2, 7, 11, 15], target = 9,

Because nums[0] + nums[1] = 2 + 7 = 9,
return [0, 1].


UPDATE (2016/2/13):
The return format had been changed to zero-based indices. Please read the above updated description carefully.
'''

#1. iterate all possible sums : time. O(n^2)
class Solution1(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        length=len(nums)
        for i in range (0,length,1):
            for j in range(i+1,length,1):
                if  (nums[i]+nums[j]) == target: return [i,j]



#2 hash the possible "partner" in advance with its index
# hash table structure: <number,partner index>

class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        length=len(nums)
        partner=dict()
        for i in range (0,length,1):
            #check whether the parter exists
            if  partner.has_key(target-nums[i]): return[partner[target-nums[i]],i  ]

            # if it has no partner, hash the current element  as a partner of others
            partner[nums[i]]=i
