"""
Given a binary tree, determine if it is a valid binary search tree (BST).

Assume a BST is defined as follows:

The left subtree of a node contains only nodes with keys less than the node's key.
The right subtree of a node contains only nodes with keys greater than the node's key.
Both the left and right subtrees must also be binary search trees.
Example 1:
    2
   / \
  1   3
Binary tree [2,1,3], return true.
Example 2:
    1
   / \
  2   3
Binary tree [1,2,3], return false.
"""
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
import sys
class Solution(object):
    def isValidBST(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        if root == None:
            return True
        else:
            upper_bound = sys.maxint
            lower_bound = -sys.maxint
            return self.isValidBst_recursive(root, lower_bound, upper_bound)

    def isValidBst_recursive(self, node, lower_bound, upper_bound):
        # node must be non empty

        left_sub = True
        if node.left:
            if not (lower_bound < node.left.val and node.left.val < node.val): return False
            new_upper_bound = upper_bound
            if node.val < new_upper_bound:
                new_upper_bound = node.val
            left_sub = self.isValidBst_recursive(node.left, lower_bound, new_upper_bound)

        right_sub = True
        if node.right:
            if not (node.val < node.right.val and node.right.val < upper_bound): return False

            new_lower_bound = lower_bound
            if node.val > new_lower_bound:
                new_lower_bound = node.val
            right_sub = self.isValidBst_recursive(node.right, new_lower_bound, upper_bound)

        return (left_sub and right_sub)


