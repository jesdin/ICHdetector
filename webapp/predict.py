from PIL import Image
import requests
from io import BytesIO
import numpy
import matplotlib.pyplot as plt

def saveInfo(name, url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # img.show()
    img = numpy.array(img)
    data = {"name" : name, "image" : img, "ICH" : None}
    return data
