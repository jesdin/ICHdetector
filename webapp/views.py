from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from PIL import Image
import requests
from io import BytesIO
import numpy
import matplotlib.pyplot as plt

# Create your views here.
def home(request):
    return render(request,'home.html')

@csrf_protect
def go_to_detector(request):
    return render(request,'detector.html')

@csrf_protect
def checkICH(request):
    print(request.POST.get("name"))
    url = request.POST.get("image")
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    print(url)
    # img.show()
    img = numpy.array(img)
    plt.show(img)
    return render(request,'detector.html')