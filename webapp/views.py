from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from webapp.predict import saveInfo

import requests
from io import BytesIO

data = {}

# Create your views here.
def home(request):
    return render(request,'home.html')

@csrf_protect
def go_to_detector(request):
    return render(request,'detector.html')

@csrf_protect
def checkICH(request):
    name = request.POST.get("name")
    url = request.POST.get("image")
    response = requests.get(url)
    blob = BytesIO(response.content)
    data = saveInfo(name, blob)
    return JsonResponse({"s": "success"}, status=200)

def results(request):
    return render(request, 'results.html')
