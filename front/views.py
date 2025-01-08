from django.shortcuts import render
from django.http import HttpResponse
from back.models import *

def home(request):
    # return HttpResponse("<h1>Bienvenue</h1>")
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True).order_by('name')
    context = {
        # 'categories': categories,
        'products': products 
    }
    return render(request, 'front/index.html', context)

def details(request):
    return render(request, 'front/details.html', {})

def shop(request):
    return render(request, 'front/shop.html', {})

def cart(request):
    return render(request, 'front/cart.html', {})

def checkout(request):
    return render(request, 'front/checkout.html', {})

def contact(request):
    return render(request, 'front/contact.html', {})