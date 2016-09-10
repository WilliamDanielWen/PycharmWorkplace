"""
key  thoughts:
1. string
2. built-in function eval()
3. built-in function  bin()
"""


class Solution(object):
    def addBinary(self, a, b):
        #learn how to use eval()
        c=eval('0b'+a)+eval('0b'+b) #turn into binary value and add
        c=bin(c)#turn into binary string
        return c[2:] #cut the '0b'