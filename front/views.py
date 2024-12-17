from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    # return HttpResponse("<h1>Bienvenue</h1>")
    return render(request, 'front/index.html', {})