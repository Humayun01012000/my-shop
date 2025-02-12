from .models import Cart
def cart(request):
    return {
        'cart': Cart.objects.filter(session_key=request.session.session_key).first()
    }