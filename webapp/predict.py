from PIL import Image
import numpy

import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior()
import keras
from keras import backend as K
import numpy as np
import cv2
import base64

from sklearn.cluster import KMeans
from skimage.color import rgb2hsv
import imutils
from io import BytesIO

global graph
graph = tf.get_default_graph() 

model = keras.models.load_model("assets/Model/weightsInception.h5")
# model = keras.models.load_model("assets/Model/ICH_Inception.h5")
# model.summary()

def saveInfo(name, blobs):
    img = [numpy.array(Image.open(blob)) for blob in blobs]
    ich = predictICH(img)
    blobs = [base64.b64encode(blob.getvalue()) for blob in blobs]
    segmented = []
    n = len(img)
    for i in range(n):
        segImg = genSegmentedImage(img[i])
        segImg = Image.fromarray(segImg)
        buffered = BytesIO()
        segImg.save(buffered, format="png")
        segmented.append(base64.b64encode(buffered.getvalue()))
        # segImg.show()
    data = {"n" : n, "name" : name, "image" : blobs, "ICH" : ich, "segmented" : segmented}
    return data

def predictICH(images):
    images = np.array([cv2.resize(image, (256, 256)) for image in images])
    K.reset_uids()
    with graph.as_default():
    	p = model.predict(images/255.)
    predicted = np.array([int(x[0] > 0.5) for x in p])
    print("Prediction : ",  predicted)
    return predicted

def genSegmentedImage(image):
    #image = cv2.resize(image, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # determine the most extreme points along the contour
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # draw the outline of the object, then draw each of the extreme points, where the left-most is red,
    # right-most is green, top-most is blue, and bottom-most is teal
    cv2.drawContours(image, [c], -1, (0, 255, 255), 2)
    cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
    cv2.circle(image, extRight, 8, (0, 255, 0), -1)
    cv2.circle(image, extTop, 8, (255, 0, 0), -1)
    cv2.circle(image, extBot, 8, (255, 255, 0), -1)
    
    #Cropping the image
    ADD_PIXELS = 0
    new_image = image[extTop[1]-ADD_PIXELS:extBot[1]+ADD_PIXELS, extLeft[0]-ADD_PIXELS:extRight[0]+ADD_PIXELS].copy()
    new_image = cv2.resize(new_image, dsize=(256, 256), interpolation=cv2.INTER_CUBIC)

    #Adjusting Contrast and Brightness of the image
    new_img = cv2.convertScaleAbs(new_image, alpha=1.7, beta=-100)

    x = np.array(new_img)

    #Stacking up the array x and rgb2hsv(x)
    z = np.dstack((x,rgb2hsv(x)))
    vectorized = np.float32(z.reshape((-1,6)))

    #Clusterin
    kmeans = KMeans(random_state=0, init='random', n_clusters=2)
    labels = kmeans.fit_predict(vectorized)

    pic = labels.reshape(z.shape[0], z.shape[1])

    pic = cv2.convertScaleAbs(pic, alpha=(255.0))
    return pic