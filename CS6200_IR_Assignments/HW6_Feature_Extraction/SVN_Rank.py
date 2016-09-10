import dlib
import pandas as pd
trainSet = pd.read_csv('runtime_cache/train_split3.csv')
testSet = pd.read_csv('runtime_cache/test_split3.csv')

trainSetFeatures = trainSet.drop(['query_id', 'doc_id', 'label','query_length'],axis=1).values
trainSetLabels = trainSet['label'].values

testSetFeatures = testSet.drop(['query_id', 'doc_id', 'label','query_length'], axis=1).values
testSetLabels = testSet['label'].values



train_data = dlib.ranking_pair()

for i in range(0,len(trainSetFeatures),1):
    if trainSetLabels[i]==1:
        train_data.relevant.append(dlib.vector(trainSetFeatures[i]))
    else:
        train_data.nonrelevant.append(dlib.vector(trainSetFeatures[i]))

import time
s_time=time.time()
svmModel = dlib.svm_rank_trainer()
svmModel.be_verbose()
svmModel.max_iterations=10
svmModel.c = 10

print "Begin trianing "
trained_model = svmModel.train(train_data)
print "Training finished!, time usage:",time.time()-s_time,"seconds."


predictedLabels =[]
for i in range(0,len(testSetFeatures),1):
    feature_vector=dlib.vector(testSetFeatures[i])
    label=trained_model(feature_vector)
    predictedLabels.append(label)

predicted_train_Labels = []
for i in range(0,len(trainSetFeatures),1):
    feature_vector = dlib.vector(trainSetFeatures[i])
    label = trained_model(feature_vector)
    predicted_train_Labels.append(label)

import Utilities
result_path = "runtime_cache/test_performance_SVM_Rank_split3.txt"
Utilities.outputResult(testSet,predictedLabels,result_path)

result_path = "runtime_cache/train_performance_SVM_Rank_split3.txt"
Utilities.outputResult(trainSet,predicted_train_Labels,result_path)

