"""
Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

For example, you may serialize the following tree

    1
   / \
  2   3
     / \
    4   5
as "[1,2,3,null,null,4,5]", just the same as how LeetCode OJ serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.
Note: Do not use class member/global/static variables to store states. Your serialize and deserialize algorithms should be stateless.

Credits:
Special thanks to @Louis1992 for adding this problem and creating all test cases.

Subscribe to see which companies asked this question
"""


# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        return self.pre_order_serialize(root)

    def pre_order_serialize(self, node):
        if node == None: return 'null'

        result=''
        result += str(node.val)
        result += ','+str(self.pre_order_serialize(node.left))
        result += ','+str(self.pre_order_serialize(node.right))
        return result

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """

        if len(data)==0: return None
        if len(data) == 1: return TreeNode(int(data[0]))
        values=data.split(',')
        return self.pre_order_deserialize(values)

    def pre_order_deserialize(self, values):
        # we make sure vlues is always none empty
        value=values.pop(0)
        if value == "null":
            return None
        else:
            parent_node=TreeNode(int(value))

            if len(values)>0:
                parent_node.left=self.pre_order_deserialize(values)

            if len(values) > 0:
                parent_node.right=self.pre_order_deserialize(values)

            return parent_node



    # Your Codec object will be instantiated and called as such:

    # codec.deserialize(codec.serialize(root))

if __name__ == '__main__':


    codec = Codec()
    root =TreeNode(1)

    result= codec.deserialize(codec.serialize(root))
    debug=1

