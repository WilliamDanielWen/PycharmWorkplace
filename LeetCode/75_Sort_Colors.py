
class Solution(object):
    def sortColors(self, nums):
        """
        :type nums: List[int]
        :rtype: void Do not return anything, modify nums in-place instead.
        """
        self.bubble_sort(nums)

    def  bubble_sort(self,nums):

        stop = False
        while  not  stop:

            stop=True
            for i in range(0,len(nums),1):
                if  not i==len(nums)-1 and nums[i]>nums[i+1]:
                    temp=nums[i]
                    nums[i]=nums[i+1]
                    nums[i+1]=temp

                    stop=False

    #def counting_sort(self,nums):
        



if  __name__=="__main__":
    s=Solution()
    test1=[0,1,2,1,0,2,2,1,1,0,1,2,2]
    s.sortColors(test1)
    print  test1