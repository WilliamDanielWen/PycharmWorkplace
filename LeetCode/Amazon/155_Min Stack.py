"""
Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

push(x) -- Push element x onto stack.
pop() -- Removes the element on top of the stack.
top() -- Get the top element.
getMin() -- Retrieve the minimum element in the stack.
Example:
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin();   --> Returns -3.
minStack.pop();
minStack.top();      --> Returns 0.
minStack.getMin();   --> Returns -2.

"""

import sys


class MinStack(object):
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.min = sys.maxint
        self.minstack = []

    def push(self, x):
        """
        :type x: int
        :rtype: void
        """
        if x <= self.min:
            self.minstack.append(self.min)
            self.min = x

        self.minstack.append(x)

    def pop(self):
        """
        :rtype: void
        """
        top = self.minstack.pop()

        if top == self.min:
            previous_min = self.minstack.pop()
            self.min = previous_min

        return top

    def top(self):
        """
        :rtype: int
        """
        return self.minstack[-1]

    def getMin(self):
        """
        :rtype: int
        """
        return self.min


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(x)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()
if __name__ == "__main__":

    minStack =MinStack()
    minStack.push(0)
    minStack.push(1)
    minStack.push(0)
    print minStack.getMin()
    minStack.pop()
    print minStack.getMin()

