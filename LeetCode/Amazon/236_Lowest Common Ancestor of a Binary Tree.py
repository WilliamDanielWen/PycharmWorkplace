# -*- coding: utf-8 -*-

"""
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia:
“The lowest common ancestor is defined between two nodes v and w as the lowest node in T that has both v and w as descendants
(where we allow a node to be a descendant of itself).”

        _______3______
       /              \
    ___5__          ___1__
   /      \        /      \
   6      _2       0       8
         /  \
         7   4
For example, the lowest common ancestor (LCA) of nodes 5 and 1 is 3.
Another example is LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.

"""

#http://bookshadow.com/weblog/2015/07/13/leetcode-lowest-common-ancestor-binary-tree/

#iterative method





# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


#recursive method
#http://stackoverflow.com/questions/27769381/how-to-find-lowest-common-ancestor-in-binary-tree-using-bottom-up-recursion
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        """
        :type root: TreeNode
        :type p: TreeNode
        :type q: TreeNode
        :rtype: TreeNode
        """
        return self.lowestCommonAncestor_recursive(root,p,q)



    def lowestCommonAncestor_recursive(self,root,p,q):


        if root == None:
            # recursion reach the bottom
            return None

        if root==p or root==q:
            return root

        right_result=self.lowestCommonAncestor(root.right, p,q)

        left_result=self.lowestCommonAncestor(root.left, p, q)


        if right_result!=None and left_result!=None:
            return root

        if right_result==None:
            return left_result
        else :
            return right_result





