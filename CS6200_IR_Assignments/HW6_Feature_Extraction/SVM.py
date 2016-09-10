
import pandas as pd
import Utilities
from sklearn import svm


trainSet = pd.read_csv('runtime_cache/train_split3.csv')
testSet = pd.read_csv('runtime_cache/test_split3.csv')

trainSetFeatures = trainSet.drop(['query_id', 'doc_id', 'label','query_length'],axis=1).values
trainSetLabels = trainSet['label'].values

testSetFeatures = testSet.drop(['query_id', 'doc_id', 'label','query_length'], axis=1).values
testSetLabels = testSet['label'].values


# build a svm trainning model
svmModel = svm.SVR(C=10000, kernel="sigmoid", tol=0.0000001,verbose=True)

# start trainning
svmModel.fit(trainSetFeatures, trainSetLabels)

# make predictions
predictedLabels = svmModel.predict(testSetFeatures)
predicted_train_Labels = svmModel.predict(trainSetFeatures)



print "MAE :\t", Utilities.getMAE(testSetLabels, predictedLabels)
print "RMSE :\t", Utilities.getRMSE(testSetLabels, predictedLabels)




result_path = "runtime_cache/test_performance_SVM_split3.txt"
Utilities.outputResult(testSet,predictedLabels,result_path)

result_path = "runtime_cache/train_performance_SVM_split3.txt"
Utilities.outputResult(trainSet,predicted_train_Labels,result_path)









