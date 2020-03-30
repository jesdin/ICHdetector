from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def go_to_detector(request):
    return render(request,'detector.html')

def checkICH(request):
    print("Ajax Complete")
    return render(request,'detector.html')
    # return render(request, )