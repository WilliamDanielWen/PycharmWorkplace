import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
import time

data_root = '/mnt/hgfs/UbuntuSharedFolder/CS6220DataMiningProjectDatasets/'

train_photos = pd.read_csv(data_root+'first_sampled_data_photo_to_biz_ids.csv')
train_photo_to_biz = pd.read_csv(data_root+'first_sampled_data_photo_to_biz_ids.csv', index_col='photo_id')

train_df = pd.read_csv(data_root+"first_sampled_data_biz_fc7features.csv")
test_df  = pd.read_csv(data_root+"second_sampled_data_biz_fc7features.csv")

y_train = train_df['label'].values
X_train = train_df['feature vector'].values
X_test = test_df['feature vector'].values

def convert_label_to_array(str_label):
    str_label = str_label[1:-1]
    str_label = str_label.split(',')
    return [int(x) for x in str_label if len(x)>0]

def convert_feature_to_vector(str_feature):
    str_feature = str_feature[1:-1]
    str_feature = str_feature.split(',')
    return [float(x) for x in str_feature]

y_train = np.array([convert_label_to_array(y) for y in train_df['label']])
X_train = np.array([convert_feature_to_vector(x) for x in train_df['feature vector']])
X_test = np.array([convert_feature_to_vector(x) for x in test_df['feature vector']])


t=time.time()

mlb = MultiLabelBinarizer()
train_set_labels= mlb.fit_transform(y_train)  #Convert list of labels to binary matrix

random_state = np.random.RandomState(0)
train_set_features, test_set_features, train_set_labels, test_set_true_labels = train_test_split(X_train, train_set_labels, test_size=.2, random_state=random_state)
classifier = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True))
classifier.fit(train_set_features, train_set_labels)

predicted_labels = classifier.predict(test_set_features)

print "Time passed: ", "{0:.1f}".format(time.time()-t), "sec"
print "F1 score: ", f1_score(test_set_true_labels, predicted_labels, average='micro')




