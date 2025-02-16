from django.shortcuts import render, get_object_or_404
from .models import Product, Category ,PopularSearch
from dal import autocomplete
from django.db.models import Q 

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


class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs



def search(request):
    # Get search parameters
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Initialize results
    results = Product.objects.all()

    # Apply search query
    if query:
        results = results.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
        # Track popular searches
        popular_search, created = PopularSearch.objects.get_or_create(query=query)
        if not created:
            popular_search.count += 1
            popular_search.save()

    # Apply category filter
    if category:
        results = results.filter(category__slug=category)

    # Apply price range filter
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)

    # Get popular searches
    popular_searches = PopularSearch.objects.order_by('-count')[:5]

    # Get no-results suggestions
    suggestions = []
    if not results and query:
        suggestions = Product.objects.filter(
            Q(name__icontains=query[:3]) | 
            Q(description__icontains=query[:3])
        )[:5]

    return render(request, 'core/search_results.html', {
        'results': results,
        'query': query,
        'categories': Category.objects.all(),
        'popular_searches': popular_searches,
        'suggestions': suggestions,
    })