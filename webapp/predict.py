from PIL import Image
import numpy
import matplotlib.pyplot as plt

import keras
import numpy as np
import cv2

model = keras.models.load_model("assets/Model/weightsInception.h5")

def saveInfo(name, blob):
    img = Image.open(blob)
    # img.show()
    img = numpy.array(img)
    ich = predictICH([img])
    data = {"name" : name, "image" : blob, "ICH" : ich}
    return data

def predictICH(images):
    images = np.array([cv2.resize(image, (256, 256)) for image in images])
    p = model.predict(images/255.)
    predicted = np.array([int(x[0] > 0.5) for x in p])
    print("Prediction : ",  predicted)
    return predicted