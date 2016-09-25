"""
17. Letter Combinations of a Phone Number  QuestionEditorial Solution  My Submissions
Total Accepted: 99240
Total Submissions: 322726
Difficulty: Medium
Given a digit string, return all possible letter combinations that the number could represent.

A mapping of digit to letters (just like on the telephone buttons) is given below.



Input:Digit string "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].
Note:
Although the above answer is in lexicographical order, your answer could be in any order you want.

Subscribe to see which companies asked this question
"""

class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        if len(digits) == 0: return []
        keyboard = dict()
        keyboard['2'] = "abc"
        keyboard['3'] = "def"
        keyboard['4'] = "ghi"
        keyboard['5'] = "jkl"
        keyboard['6'] = "mno"
        keyboard['7'] = "pqrs"
        keyboard['8'] = "tuv"
        keyboard['9'] = "wxyz"

        previous_result = [""]
        for digit in digits:
            new_letters = keyboard[digit]
            new_result = []
            for combination in previous_result:
                for letter in new_letters:
                    new_result.append(combination + letter)
            previous_result = new_result

        return previous_result

if __name__ == "__main__":
    s = Solution()

    digits = ""
    print s.letterCombinations(digits)