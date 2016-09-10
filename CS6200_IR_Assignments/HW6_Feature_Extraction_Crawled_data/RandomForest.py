import pandas as pd
import Utilities
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor

# read the data that we need from the original file
trainSet = pd.read_csv('runtime_cache/train.csv')
testSet = pd.read_csv('runtime_cache/test.csv')

trainSetFeatures = trainSet.drop(['query_id', 'doc_id', 'label',"query_length"],axis=1).values
trainSetLabels = trainSet['label'].values

testSetFeatures = testSet.drop(['query_id', 'doc_id', 'label','query_length'], axis=1).values
testSetLabels = testSet['label'].values




print "\nBegin training..."
#train the model
random_forest_regressor = RandomForestRegressor(n_estimators=15, max_depth=8, random_state=10)
bagging_regressor = BaggingRegressor(random_forest_regressor, n_estimators=50, max_samples=0.1, random_state=25)
bagging_regressor.fit(trainSetFeatures, trainSetLabels)

print "\nBegin prediction..."
#make the prediction on the test set
predictedLabels = bagging_regressor.predict(testSetFeatures)
predicted_train_Labels = bagging_regressor.predict(trainSetFeatures)



print "RMSE :\t", Utilities.getRMSE(testSetLabels, predictedLabels)
print "MAE :\t", Utilities.getMAE(testSetLabels, predictedLabels)



result_path = "runtime_cache/test_performance_random_forest.txt"
Utilities.outputResult(testSet,predictedLabels,result_path)

result_path = "runtime_cache/train_performance_random_forest.txt"
Utilities.outputResult(trainSet,predictedLabels,result_path)
