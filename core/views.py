from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'core/home.html', {
        'products': products,
        'categories': categories
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'core/product_detail.html', {'product': product})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'core/category_list.html', {
        'category': category,
        'products': products
    })