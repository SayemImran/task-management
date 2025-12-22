from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    # return render(request,"home.html")
    return render(request,'home.html')

def no_permission(request):
    return render(request,'no_permission.html')