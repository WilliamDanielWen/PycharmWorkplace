"""
You are given an n x n 2D matrix representing an image.

Rotate the image by 90 degrees (clockwise).

Follow up:
Could you do this in-place?
"""
class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: void Do not return anything, modify matrix in-place instead.
        """
        for i in range(len(matrix)):
            for j in range(i, len(matrix)):
                # trnaspose the matrix
                temp = matrix[i][j]
                matrix[i][j] = matrix[j][i]
                matrix[j][i] = temp

        for i in range(len(matrix)):
            for j in range(0, len(matrix) / 2):
                # flip horizontally
                temp = matrix[i][j]
                matrix[i][j] = matrix[i][-(j + 1)]
                matrix[i][-(j + 1)] = temp