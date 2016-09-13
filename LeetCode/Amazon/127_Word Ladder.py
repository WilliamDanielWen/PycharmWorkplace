"""
Given two words (beginWord and endWord), and a dictionary's word list
, find the length of shortest transformation sequence from beginWord to endWord, such that:

Only one letter can be changed at a time
Each intermediate word must exist in the word list
For example,

Given:
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log"]
As one shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog",
return its length 5.

Note:
Return 0 if there is no such transformation sequence.
All words have the same length.
All words contain only lowercase alphabetic characters.
"""

class Solution(object):
    def ladderLength(self, beginWord, endWord, wordList):
        """
        :type beginWord: str
        :type endWord: str
        :type wordList: Set[str]
        :rtype: int
        """
        return self.bidirectional_bfs(beginWord,endWord,wordList)

    def bidirectional_bfs(self,start,end,graph):
        import string
        """
                :type beginWord: str
                :type endWord: str
                :type wordList: Set[str]
                :rtype: int
        """
        if start==end: return 1

        path_length=1

        large_frontier=set()
        small_frontier=set()
        visited_set=set()
        visited_set.add(start)
        visited_set.add(end)


        small_frontier.add(start) # word that is not target
        large_frontier.add(end) # word that is not sart

        while(len(large_frontier)>0 and len(small_frontier)>0):
                # only expand the samll frontier to restrict the time complexity
                if len(small_frontier)> len(large_frontier):
                    temp =small_frontier
                    small_frontier = large_frontier
                    large_frontier = temp

                smallFrontier_neighbors = set()

                #explore every word in small frontier
                for word in small_frontier:


                    # word is not in the large_frontier substitute every character with 26 alphabet lowercase letter
                    word_array = list(word)
                    for i in range(0,len(word_array)):

                        original_letter=word_array[i]
                        for new_letter in string.ascii_lowercase:

                            word_array[i] = new_letter
                            new_word = ''.join(word_array)

                            if new_word in large_frontier:
                                return path_length+1

                            if (new_word in graph) and (not new_word in visited_set) :
                                smallFrontier_neighbors.add(new_word)
                                visited_set.add(new_word)


                            word_array[i]=original_letter

                #update frontier
                small_frontier=smallFrontier_neighbors

                # begin nex level search
                path_length += 1

        # search failed
        return 0


if __name__=="__main__":
    start="a"
    end="c"
    graph=["a", "b", "c"]

    start="hot"
    end="dog"
    graph=["hot", "dog", "dot"]

    s=Solution()
    print s.ladderLength(start,end,graph)
