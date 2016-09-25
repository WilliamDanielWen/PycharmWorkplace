"""
Given a string s and a dictionary of words dict, determine if s can be segmented into a space-separated sequence of one or more dictionary words.

For example, given
s = "leetcode",
dict = ["leet", "code"].

Return true because "leetcode" can be segmented as "leet code".

"""

class Solution(object):
    def wordBreak(self, s, wordDict):
        """
        :type s: str
        :type wordDict: Set[str]
        :rtype: bool
        """
        length = len(s)
        if length == 0 : return False
        dp = [False] * (length + 1)
        dp[0] = True
        for end in range(1, length + 1):

            # fix the and scan throuhg the start
            for start in reversed(range(end)): #(start<end)
                if dp[start] and (s[start:end] in wordDict):
                    # substring is s[start,end), which didn't include s[end]
                    dp[end] = True
                    break  # match found, stop the scan

        return dp[length]






s="leet code"
s=""
s= "l"
s= "leetcode"
dict=set()
dict.add("leet")
dict.add("code")
sol=Solution()
print sol.wordBreak(s,dict)
