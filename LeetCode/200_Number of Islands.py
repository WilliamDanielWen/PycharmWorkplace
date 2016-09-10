'''
Given a 2d grid map of '1's (land) and '0's (water), count the number of islands.
An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.
You may assume all four edges of the grid are all surrounded by water.

Example 1:

11110
11010
11000
00000
Answer: 1

Example 2:

11000
11000
00100
00011
Answer: 3
'''


class Solution(object):
    def numIslands(self, grid):
        """
        :type grid: List[List[str]]
        :rtype: int
        """
        # import copy
        # grid=copy.deepcopy(grid)

        count =0
        for i in range(0,len(grid)):
            for j in range(0,len(grid[i])):

                if grid[i][j]=='1':
                    count +=1
                    self.sink(grid,i,j)

        return count

    def sink(self,grid,i,j):


        if not (0<=i and i<=len(grid)-1 and 0<=j and j<=len(grid[i])-1):
            return # out of boundry

        if grid[i][j]=='0':
                return

        grid[i][j]='0'
        self.sink(grid, i+1 ,j)
        self.sink(grid, i-1 , j)
        self.sink(grid, i   , j-1)
        self.sink(grid, i   , j+1)


if __name__=="__main__":
    s=Solution()
    grid =[  ['1','1','1','1','0']
            ,['1','1','0','1','0']
            ,['1','1','0','0','0']
            ,['0','0','0','0','0']]

    grid = [['1', '1', '0', '0', '0']
        , ['1', '1', '0', '0', '0']
        , ['0', '0', '1', '0', '0']
        , ['0', '0', '0', '1', '1']]
    print s.numIslands(grid)