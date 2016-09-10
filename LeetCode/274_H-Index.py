class Solution(object):
    def hIndex(self, citations):
        """
        :type citations: List[int]
        :rtype: int
        """
        if citations==None or len(citations) == 0:
            return 0

        h_index=0
        citations = sorted(citations, reverse=True)
        for i in range(0,len(citations),1):
            #last index
            if   i==len(citations)-1:
                h_index = min(i+1,citations[i])
                break

            if citations[i]>=i+1 and i +1>=citations[i+1]:
                h_index=i+1
                break

        return h_index

if __name__=="__main__":
    sol=Solution()
    citations=[1,5,6,9,30,58,20,59,4,5,0,10,0,3]
    citations =[]
    #citations = [0,0,0,0,0,0]
    print sol.hIndex(citations)
    print sorted(citations,reverse=True)
    print range(1,len(citations)+1,1)