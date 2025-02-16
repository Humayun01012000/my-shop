# cart/views.py
from django.shortcuts import render,get_object_or_404, redirect
from core.models import Product
from .models import Cart, CartItem 
from django.contrib.auth.decorators import login_required

def _get_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

@login_required
def add_to_cart(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    cart = _get_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = _get_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart:cart_detail')