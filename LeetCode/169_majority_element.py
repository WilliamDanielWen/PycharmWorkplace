
"""
Key Thoughts:
1. majority vote algorithm
2. #https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_majority_vote_algorithm
3. #https://leetcode.com/discuss/24971/o-n-time-o-1-space-fastest-solution
   #the majority vote problem
"""
class Solution(object):
    def majorityElement(self, nums):
        major=nums[0]
        times=1
        for  i in  range(1,len(nums),1):
            if  not times==0:
            #still think some element could be the major
                if major == nums[i]:
                    # still hit
                    times += 1
                else:
                    #miss
                    times -= 1

            else :
                # one element is canceled out, set another new start
                major = nums[i]
                times = 1

        return major