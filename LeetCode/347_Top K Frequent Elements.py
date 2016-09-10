"""
Given a non-empty array of integers, return the k most frequent elements.

For example,
Given [1,1,1,2,2,3] and k = 2, return [1,2].


"""
import heapq
class Solution(object):
    def topKFrequent(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """

        # O(n)
        freq={}
        for num in nums:
            if freq.has_key(num):
                freq[num]-=1
            else:
                freq[num]=0

        # <O(n)
        freq_lst=[]
        for num in freq:
            freq_lst.append( (freq[num], num) )

        heapq.heapify(freq_lst)

        #nlog(n)
        k_most=[]
        for i in range(0,k):
            k_most.append(heapq.heappop(freq_lst)[1])

        return k_most


if __name__=="__main__":
    s=Solution()
    nums=[1, 1, 1, 2, 2, 3]
    k=2
    print s.topKFrequent(nums,k)