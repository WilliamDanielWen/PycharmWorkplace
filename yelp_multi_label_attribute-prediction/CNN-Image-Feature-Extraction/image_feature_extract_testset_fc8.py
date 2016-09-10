import numpy as np
import caffe
import os

#complied caffe python wraper should be here, every computer is different
compiled_caffe_location = '/home/daniel/caffe/'

#all related phtos and files should be here, every computer is different
data_folder_location = '/mnt/hgfs/UbuntuSharedFolder/CS6220DataMiningProjectDatasets/'

# Use CPU
caffe.set_mode_cpu()

#loop on
def get_fc8_feature(images, layer ='fc8'):
    preTrianedCaffeNet = caffe.Net(compiled_caffe_location + 'models/bvlc_reference_caffenet/deploy.prototxt',
                    compiled_caffe_location + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel',
                    caffe.TEST)

    caffe_preprocessor = caffe.io.Transformer({'data': preTrianedCaffeNet.blobs['data'].data.shape})
    caffe_preprocessor.set_transpose('data', (2,0,1))
    caffe_preprocessor.set_mean('data', np.load(compiled_caffe_location + 'python/caffe/imagenet/ilsvrc_2012_mean.npy').mean(1).mean(1)) # set mean
    caffe_preprocessor.set_raw_scale('data', 255)  # set range to in [0,255]
    caffe_preprocessor.set_channel_swap('data', (2,1,0))  # set channel order to BGR order instead of RGB]]

    num_images= len(images)
    preTrianedCaffeNet.blobs['data'].reshape(num_images,3,227,227)
    preTrianedCaffeNet.blobs['data'].data[...] = map(lambda x: caffe_preprocessor.preprocess('data',caffe.io.load_image(x)), images)
    preTrianedCaffeNet.forward()# feedforward to calculate the feature

    return preTrianedCaffeNet.blobs[layer].data


# save it to hd5 file
# Initialize files
import h5py
f = h5py.File(data_folder_location + 'second_sampled_data_image_fc8features.h5', 'w')
filenames = f.create_dataset('photo_id',(0,), maxshape=(None,),dtype='|S54')
feature = f.create_dataset('feature',(0,4096), maxshape = (None,4096))
f.close()

import pandas as pd
photos_indexes = pd.read_csv(data_folder_location + 'second_sampled_data_photo_to_biz_ids.csv')
photo_location = data_folder_location + 'train_photos/'
photo_set = [os.path.join(photo_location, str(x) + '.jpg') for x in photos_indexes['photo_id']]  # get full filename

num_train = len(photo_set)
print "Number of training images: ", num_train

batch_size = 500
import time
start = time.time()

#process images
for i in range(0, num_train, batch_size):
    images = photo_set[i: min(i + batch_size, num_train)]
    features = get_fc8_feature(images, layer='fc8')
    num_done = i+features.shape[0]
    f= h5py.File(data_folder_location + 'second_sampled_data_image_fc8features.h5', 'r+')
    f['photo_id'].resize((num_done,))
    f['photo_id'][i: num_done] = np.array(images)
    f['feature'].resize((num_done,features.shape[1]))
    f['feature'][i: num_done, :] = features
    f.close()
    if num_done%batch_size==0 or num_done==num_train:
        print "Images processed: ", num_done, "Time passed: ", "{0:.1f}".format(time.time()-start), "sec"


