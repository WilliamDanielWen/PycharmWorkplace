"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.
"""


class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        stack = []
        for char in s:
            if char == "(" or char == "[" or char == "{":
                stack.append(char)

            elif len(stack) == 0:
                return False
            elif char == ")":
                recent = stack.pop()
                if recent != "(": return False

            elif char == "]":
                recent = stack.pop()
                if recent != "[": return False

            elif char == "}":
                recent = stack.pop()
                if recent != "{": return False

        if len(stack) != 0: return False

        return True

if __name__ == "__main__" :
    sol = Solution()
    s = "()[]{}(())[]{{[]}}"
    print sol.isValid(s)