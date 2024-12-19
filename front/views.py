from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
  #  return HttpResponse("<h1>Bienvenue !!</h1>")
  return render(request, 'front/index.html',{})
def details(request):
  return render(request, 'front/details.html',{})

def shop(request):
      return render(request, 'front/shop.html',{})

def contact(request):
      return render(request, 'front/contact.html',{})

def cart(request):
      return render(request, 'front/cart.html',{})

def checkout(request):
      return render(request, 'front/checkout.html',{})


