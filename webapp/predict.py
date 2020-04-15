from PIL import Image
import numpy

import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import keras
from keras import backend as K
import numpy as np
import cv2

global graph
graph = tf.get_default_graph() 

model = keras.models.load_model("assets/Model/weightsInception.h5")
# model.summary()

def saveInfo(name, blob):
    img = Image.open(blob)
    # img.show()
    img = numpy.array(img)
    ich = predictICH([img])
    data = {"name" : name, "image" : blob, "ICH" : ich}
    return data

def predictICH(images):
    images = np.array([cv2.resize(image, (256, 256)) for image in images])
    K.reset_uids()
    with graph.as_default():
    	p = model.predict(images/255.)
    predicted = np.array([int(x[0] > 0.5) for x in p])
    print("Prediction : ",  predicted)
    return predicted