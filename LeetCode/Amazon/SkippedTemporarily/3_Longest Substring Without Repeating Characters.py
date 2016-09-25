'''
Given a string, find the length of the longest substring without repeating characters.

Examples:

Given "abcabcbb", the answer is "abc", which the length is 3.

Given "bbbbb", the answer is "b", with the length of 1.

Given "pwwkew", the answer is "wke", with the length of 3. Note that the answer must be a substring, "pwke" is a subsequence and not a substring.

Subscribe to see which companies asked this question
'''


class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        length = len(s)
        max_length = 0
        for i in range(length):
            chars = dict()
            str_found = ""
            for j in range(i, length):
                if not chars.has_key(s[j]):
                    chars[s[j]] = 1
                    str_found += s[j]
                else:
                    break
            if len(str_found) > max_length:
                max_length = len(str_found)

        return max_length


