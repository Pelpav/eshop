from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return HttpResponse("<h1>Bienvenue</h1>")
    return render(request, 'front/index.html', {})

def details(request):
    return render(request, 'front/details.html', {})

def shop(request):
    return render(request, 'front/shop.html', {})