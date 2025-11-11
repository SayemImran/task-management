from django.shortcuts import render
from django.http import HttpResponse

def show_default(request):
    return HttpResponse("<h1>Welcome to task Management User pannel</h1>")
