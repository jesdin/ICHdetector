from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from webapp.predict import saveInfo
from django.http import HttpResponse
import requests
from io import BytesIO


# Create your views here.
def home(request):
    return render(request,'home.html')

@csrf_protect
def go_to_detector(request):
    return render(request,'detector.html')

@csrf_protect
def checkICH(request):
    name = request.POST.get("name").split("~")
    urls = request.POST.get("image").split("~")
    blob = []
    for url in urls:
        response = requests.get(url)
        blob.append(BytesIO(response.content))
    global data
    data = saveInfo(name, blob)
    return JsonResponse({"s": "success"}, status=200)
@csrf_protect
def results(request):
    # print(data)
    return render(request,'results.html',data)
