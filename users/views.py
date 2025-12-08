from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, CustomRegistrationForm
from django.contrib.auth import authenticate, login,logout
def show_default(request):
    return HttpResponse("<h1>Welcome to task Management User pannel</h1>")

def sign_up(request):   
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign-in")
    else:
        form = CustomRegistrationForm()
    return render(request,"register.html",{"form":form})

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("doc ", username,password)
        user = authenticate(request,username=username, password=password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,"login.html")