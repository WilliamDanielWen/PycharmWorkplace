
import pandas as pd
import utils
from sklearn.linear_model import LinearRegression

# read the data that we need from the original file
trainSet = pd.read_csv('IOFolder\digit-train.csv', encoding="ISO-8859-1")
testSet = pd.read_csv('IOFolder\digit-test.csv', encoding="ISO-8859-1")

trainSetFeatures = trainSet.drop(['label'], axis=1).values #id and relevance is not features to use
trainSetLabels = trainSet['label'].values

testSetFeatures = testSet.drop(['label'], axis=1).values
testSetLabels = testSet['label'].values




#train the model
lr = LinearRegression(normalize=True)
lr.fit(trainSetFeatures, trainSetLabels)

#make the prediction on the test set
predictedLabels = lr.predict(testSetFeatures)

#output the prediction
id_test = testSet['id']
pd.DataFrame({"id": id_test, "relevance": predictedLabels}).to_csv('Linear_Regression_Results.csv', index=False)

print ("RMSE :\t", utils.getRMSE(testSetLabels, predictedLabels))
print ("MAE :\t", utils.getMAE(testSetLabels, predictedLabels))

