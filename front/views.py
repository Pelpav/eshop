from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from back.models import *

def home(request):
    # return HttpResponse("<h1>Bienvenue</h1>")
    categories = Category.objects.filter(active=True)
    products = Product.objects.filter(active=True).order_by('name')
    arrivals = Arrival.objects.filter(is_closed=False)
    arrivals_details = []
    for arrival in arrivals:
        arrivals_details += list(ArrivalDetails.objects.filter(arrival=arrival))

    context = {
        # 'categories': categories,
        'products': products,
        'arrivals_details': arrivals_details
    }
    return render(request, 'front/index.html', context)

def details(request):
    return render(request, 'front/details.html', {})

def shop(request, cat_slug='all'):
    if cat_slug == 'all':
        products = Product.objects.filter(active=True)
    else:
        products = Product.objects.filter(category__slug=cat_slug, active=True)
    perpage = request.GET.get('per', 6)
    paginator = Paginator(products, perpage)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {
        'products' : products,
    }
    return render(request, 'front/shop.html', context)

def cart(request):
    return render(request, 'front/cart.html', {})

def checkout(request):
    return render(request, 'front/checkout.html', {})

def contact(request):
    return render(request, 'front/contact.html', {})