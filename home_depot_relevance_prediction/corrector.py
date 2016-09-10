import numpy as np
import re
import pandas as pd
import collections

# help to combine two files together
def combine_files():
    filenames = ['IOFolder/big.txt', 'IOFolder/products_info.txt']
    with open('IOFolder/newBig.txt', 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

# done the combine, get new file called newBig.txt
# combine_files()

NWORDS = train(words(file('IOFolder/newBig.txt').read()))

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
   splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
   replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts = [a + c + b for a, b in splits for c in alphabet]

   return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

# load data from the file, return feature matrix and label matrix
def loadData(fileName):
    M = []

    file = open(fileName, "r")
    lines = file.readlines()

    for line in lines[1:]:
        rowLst = line.split(",")
        temp = []
        id = int(rowLst[0])
        uid = int(rowLst[1])
        length_title = len(rowLst[2])
        title = rowLst[2][1:length_title - 1]
        length_search = len(rowLst[3])
        search = rowLst[3][1:length_search - 1]

        relevance = rowLst[4]

        temp.append(id)
        temp.append(uid)
        temp.append(title)
        temp.append(search)
        temp.append(relevance)

        M.append(temp)

    return np.array(M)

# M = loadData("dataset/train.csv")
# print M[0:20]

trainSet = pd.read_csv("IOFolder/train.csv")
testSet = pd.read_csv("IOFolder/test.csv")
trainSize = trainSet.shape[0]
testSize = testSet.shape[0]

print trainSize
print testSize

print "start train"
for index in range(trainSize):
    temp = trainSet['search_term'][index]
    arr = temp.split(" ")
    newTemp = ""
    for item in arr:
        newTemp += correct(item) + " "
    length = len(newTemp)
    trainSet.set_value(index, 'search_term', newTemp[0:length - 1])

print "start test:"
for index in range(testSize):
    temp = testSet['search_term'][index]
    arr = temp.split(" ")
    newTemp = ""
    for item in arr:
        newTemp += correct(item) + " "
    length = len(newTemp)
    testSet.set_value(index, 'search_term', newTemp[0:length - 1])

print "save dataframe:"
pd.DataFrame({"id": trainSet['id'],
              "product_uid": trainSet['product_uid'],
              "product_title": trainSet['product_title'],
              "search_term": trainSet['search_term'],
              "relevance": trainSet['relevance']}).to_csv('IOFolder/newTrain.csv', index=False)

pd.DataFrame({"id": testSet['id'],
              "product_uid": testSet['product_uid'],
              "product_title": testSet['product_title'],
              "search_term": testSet['search_term']}).to_csv('IOFolder/newTest.csv', index=False)








