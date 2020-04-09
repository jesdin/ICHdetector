from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
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
    return render(request,'detector.html')