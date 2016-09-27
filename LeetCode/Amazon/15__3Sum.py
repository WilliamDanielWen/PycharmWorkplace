"""
15. 3Sum  QuestionEditorial Solution  My Submissions
Total Accepted: 146125
Total Submissions: 728741
Difficulty: Medium
Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.

Note: The solution set must not contain duplicate triplets.

For example, given array S = [-1, 0, 1, 2, -1, -4],

A solution set is:
[
  [-1, 0, 1],
  [-1, -1, 2]
]
"""


class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """

        length = len(nums)
        if length < 3:
            return []

        #make the number in an ascending order
        nums.sort()

        res = []
        for i in range(length - 2):
            if (i!=0 and nums[i] == nums[i-1]): continue # avoid repetition of 3 sum
            first_num = nums[i]
            target =  -nums[i]

            # search for all the two sum
            start = i+1
            temp_res = self.get_all_twoSums(nums, first_num, length, start, target)
            if len(temp_res) > 0:
                for tuple in temp_res:
                    res.append(tuple)

        return res

    def get_all_twoSums(self, nums, first_num, length, start, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        res = []

        l = start
        r = length - 1

        while (l < r):
            s = nums[l] + nums[r]
            if s == target:
                res.append([first_num, nums[l], nums[r]])

                #keep looking for another two sum
                l += 1
                # avoid repetition of two sum
                while(l<r and nums[l]==nums[l-1]): l +=1

            elif s < target:
                # make the sum larger according to the sorted list
                l += 1
            else:
                # make the sum smaller according to the sorted list
                r -= 1

        return res

nums=[-1, 0, 1, 2, -1, -4]
sol=Solution()
print sol.threeSum(nums)