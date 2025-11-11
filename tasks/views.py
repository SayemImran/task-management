from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def onload(request):
    return HttpResponse("<h1>Hi there</h1>")
def home(request):
    return HttpResponse("Welcome to the task management System")
