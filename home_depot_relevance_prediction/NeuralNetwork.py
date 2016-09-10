
import pandas as pd
import utils

from sknn.mlp import  Layer, Regressor

# read the data that we need from the original file
trainSet = pd.read_csv('IOFolder\digit-train.csv', encoding="ISO-8859-1")
testSet = pd.read_csv('IOFolder\digit-test.csv', encoding="ISO-8859-1")

trainSetFeatures = trainSet.drop(['label'], axis=1).values #id and relevance is not features to use
trainSetLabels = trainSet['label'].values

testSetFeatures = testSet.drop(['label'], axis=1).values
testSetLabels = testSet['label'].values


print "\nBegin training..."
#train the model
hidLayer1=Layer(type="Sigmoid",units=10)
outputLayer=Layer(type="Softmax",units=1)
network_topology=[hidLayer1,outputLayer]
feedforwardNN=Regressor(layers=network_topology)
print "\nBegin fit..."
feedforwardNN.fit(trainSetFeatures,trainSetLabels)


print "\nBegin prediction..."
#make the prediction on the test set
predictedLabels = feedforwardNN.predict(testSetFeatures)

print "\nOutput the result..."
#output the prediction
testSetId = testSet['id']
pd.DataFrame({"id": testSetId, "relevance": predictedLabels}).to_csv('IOFolder/neural_network_results.csv', index=False)

print "RMSE :\t", utils.getRMSE(testSetLabels, predictedLabels)
print "MAE :\t", utils.getMAE(testSetLabels, predictedLabels)