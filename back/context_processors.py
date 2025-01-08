from .models import Category

def getCategories(request):
    categories = Category.objects.filter(active=True).order_by('name')
    return {'categories': categories}