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

def details(request, prod_slug):
    product = Product.objects.get(slug=prod_slug)
    sim_products = list(Product.objects.filter(category=product.category, active=True).filter(active=True)[:5])
    best_liked = list(Product.objects.filter(active=True))
    best_liked.sort(key=lambda prod : prod.likes_total, reverse=True)
    for prod in sim_products:
        if prod in best_liked:
            best_liked.remove(prod)
    sim_products += best_liked[:5]
    best_rated = list(Product.objects.filter(active=True))
    best_rated.sort(key=lambda prod : prod.reviews_rate, reverse=True)
    for prod in sim_products:
        if prod in best_rated:
            best_rated.remove(prod)
    sim_products += best_rated[:5]
    context = {
        'product': product,
        'sim_products': sim_products,
    }
    return render(request, 'front/details.html', context)

def shop(request, cat_slug='all'):
    if cat_slug == 'all':
        products = Product.objects.filter(active=True)
    else:
        products = Product.objects.filter(category__slug=cat_slug, active=True)
    query = request.GET.get('q', '')
    if query:
        products = products.filter(name__icontains=query)
    sort = request.GET.get('sort', 'latest')
    if sort == 'popular':
        products = products.order_by('-likes_total')
    elif sort == 'best':
        products = products.order_by('-reviews_rate')
    perpage = request.GET.get('per', 12)
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