from .models import *
from .views import _cart_id
def counter (request):
    cart_count=0
    # if 'admin' in request.path:
    #     {}
    # else :
    try:
        cart=Cart.objects.filter(cart_id=_cart_id(request))
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user)
        else:
            cart_items=CartItem.objects.filter(cart=cart[0:1]) # عناصر العربي اللي ف العربيه الواحده و الاولي
        for cart_item in cart_items :
            cart_count+=cart_item.quantity
    except Cart.DoesNotExist :
        cart_count=0
    return dict (cart_count=cart_count)
