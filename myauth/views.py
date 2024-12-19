from django.shortcuts import render

def login(request):
    return render(request, 'myauth/login.html', {})

def register(request):
    return render(request, 'myauth/register.html', {})