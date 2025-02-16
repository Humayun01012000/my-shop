from django.urls import path
from . import views 
from core.views import ProductAutocomplete


app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_list, name='category_list'), 

     path('product-autocomplete/', ProductAutocomplete.as_view(), name='product-autocomplete'),
]