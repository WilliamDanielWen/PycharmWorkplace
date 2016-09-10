from skimage.feature import hog
from skimage.transform import resize
from skimage import io, data, color, exposure
from sklearn import svm, datasets
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import f1_score
import pandas as pd
import matplotlib.pyplot as plt
import os
import time
import numpy as np
import h5py

root = '/mnt/hgfs/UbuntuSharedFolder/CS6220DataMiningProjectDatasets/'
f = h5py.File(root+'HOGfeatures.h5','w')
filenames = f.create_dataset('photo_id',(0,), maxshape=(None,),dtype='|S54')
feature = f.create_dataset('feature',(0,2048), maxshape = (None,2048))
f.close()
train_photos = pd.read_csv(root+'train_photo_to_biz_ids.csv')   #
train_folder = root+'train_photos/'
train_images = [os.path.join(train_folder, str(x)+'.jpg') for x in train_photos['photo_id']]
totalImages=len(train_images)

for i in range(0, totalImages):     #for loop to extract feature
	im=color.rgb2gray(io.imread(train_images[i]))
	im=resize(im,(256,256))
	feature=hog(im,orientations=8,pixels_per_cell=(16, 16), cells_per_block=(1, 1))
	num = i+1
	f= h5py.File(root+'HOGfeatures.h5','r+')
	f['photo_id'].resize((num,))
	f['photo_id'][i] = train_images[i]
	f['feature'].resize((num,feature.shape[0]))
	f['feature'][i, :] = feature
	f.close()
#here takw about 14,000 seconds to extract features from all 230,000 images

train_photo_to_biz = pd.read_csv(root+'train_photo_to_biz_ids.csv')    #assign business label to features
train_labels = pd.read_csv(root+'train.csv').dropna()
train_labels['labels'] = train_labels['labels'].apply(lambda x: tuple(sorted(int(t) for t in x.split())))
train_labels.set_index('business_id', inplace=True)
biz_ids = train_labels.index.unique()
f = h5py.File(root+'HOGfeatures.h5','r')
train_image_features = np.copy(f['feature'])
f.close()
df = pd.DataFrame(columns=['business','label','feature vector'])
index = 0


def lta(label):    #a function to make label to array
    label = label[1:-1]
    label = label.split(',')
    return [int(x) for x in label if len(x)>0]
    
def ftv(feature):    # a function to make feature to vector
    feature = feature[1:-1]
    feature = feature.split(',')
    return [float(x) for x in feature]

for biz in biz_ids:          #assign business label to images
    label = train_labels.loc[biz]['labels']
    image_index = train_photo_to_biz[train_photo_to_biz['business_id']==biz].index.tolist()
    folder = root+'train_photo_folders/'
    features = train_image_features[image_index]
    mean_feature =list(np.mean(features,axis=0))
    df.loc[index] = [biz, label, mean_feature]
    index+=1


train_photos = pd.read_csv(root+'train_photo_to_biz_ids.csv')
train_photo_to_biz = pd.read_csv(root+'train_photo_to_biz_ids.csv', index_col='photo_id')
train_pd = pd.read_csv(root+"HOGfeatures.csv")

y_train = train_pd['label'].values
x_train = train_pd['feature vector'].values
y_train = np.array([lta(y) for y in train_pd['label']])
x_train = np.array([ftv(x) for x in train_pd['feature vector']])


# for label in train_pd['feature vector']:
# 	label=label[1:-1]
# 	label=label.split(',')
# 	x_train = np.array([float(float_label) for float_label in label])

# for label in train_pd['label']:
# 	label=label[1:-1]
# 	label=label.split(',')
# 	y_train=for intlabel in label:
# 		if len(intlabel)>0:
# 			intlabel=int(intlabel)

random_state = np.random.RandomState(0)
#multilabel binarizer is a method to transfer matrix to binary matrix.
mlb = MultiLabelBinarizer()
mlbtrain_y= mlb.fit_transform(y_train) 
mlbtrain_x, mlbtest_x, mlbtrain_y, mlbtest_y = train_test_split(x_train, mlbtrain_y, test_size=.2,random_state=random_state)


#using SVM combining with one vs rest classifier to predict the labels of image.
model = OneVsRestClassifier(svm.SVC(kernel='linear', probability=True))
model.fit(mlbtrain_x, mlbtrain_y)
predict = model.predict(mlbtest_x)

print "F1 score: ", f1_score(mlbtest_y, predict, average='micro')
#the final result of f1 score is 0.716701275586.