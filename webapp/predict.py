from PIL import Image
import numpy

import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import keras
from keras import backend as K
import numpy as np
import cv2
import base64

global graph
graph = tf.get_default_graph() 

model = keras.models.load_model("assets/Model/weightsInception.h5")
# model.summary()

def saveInfo(name, blobs):
    
    img = [numpy.array(Image.open(blob)) for blob in blobs]
    # seg_img = segmented(img)
    ich = predictICH(img)
    # print(f'ICH:{ich}')
    blobs = [base64.b64encode(blob.getvalue()) for blob in blobs]
    data = {"name" : name, "image" : blobs, "ICH" : ich}
    return data

def predictICH(images):
    images = np.array([cv2.resize(image, (256, 256)) for image in images])
    K.reset_uids()
    with graph.as_default():
    	p = model.predict(images/255.)
    predicted = np.array([int(x[0] > 0.5) for x in p])
    # print(predicted[0])
    if(predicted[0] == 1):
        predicted = 'HEMORRHAGE DETECTED'
    else:
        predicted = 'HEMORRHAGE NOT DETECTED'
    print("Prediction : ",  predicted)
    return predicted