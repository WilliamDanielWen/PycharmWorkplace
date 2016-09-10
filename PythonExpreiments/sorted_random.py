import  random
testDict={}
testDict[1]=['a','b','c','d','e']
testDict[3]=['a','b','c','d','e']
testDict[5]=['a','b','c','d','e']
testDict[7]=['a','b','c','d','e']
testDict[9]=['a','b','c','d','e']



keys=testDict.keys()
key_sorted = sorted(testDict.keys(), key=lambda  *args: random.random())


print  'unsorted'
for key in keys:
    print key

print 'sorted'
for key in key_sorted:
    print key
