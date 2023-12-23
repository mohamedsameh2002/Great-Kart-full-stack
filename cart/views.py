from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product,Variation
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id (request):
    cart=request.session.session_key
    if not cart :
        cart=request.session.create()
    return cart

def add_cart (request,prod_id):
    url=request.META.get('HTTP_REFERER')
    currnt_user=request.user
    product=Product.objects.get(id=prod_id)
    if currnt_user.is_authenticated:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key=item
                value=request.POST[key]

                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        
        is_cart_item_exist=CartItem.objects.filter(product=product,user=currnt_user).exists()
        if is_cart_item_exist:
            cart_item=CartItem.objects.filter(product=product,user=currnt_user)
            #existing veriation list
            ex_ver_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_ver_list.append(list (existing_variation))
                id.append(item.id)
                
            if product_variation in ex_ver_list :
                # incerment
                idex=ex_ver_list.index(product_variation)
                item_id=id[idex]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()
                messages.info(request,'the order has been updated')

            else:
                item=CartItem.objects.create(product=product,quantity=1,user=currnt_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
                messages.success(request,'the order has been added')
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                user=currnt_user,
                )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
            messages.success(request,'the order has been added')
        return redirect(url)
    
# if user is not authantecated
    else:
        product_variation=[]
        if request.method == 'POST':
            for item in request.POST:
                key=item
                value=request.POST[key]

                try:
                    variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        
        is_cart_item_exist=CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exist:
            cart_item=CartItem.objects.filter(product=product,cart=cart)
            #existing veriation list
            ex_ver_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variation.all()
                ex_ver_list.append(list (existing_variation))
                id.append(item.id)
                
            if product_variation in ex_ver_list :
                # incerment
                idex=ex_ver_list.index(product_variation)
                item_id=id[idex]
                item=CartItem.objects.get(product=product,id=item_id)
                item.quantity+=1
                item.save()

            else:
                item=CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                item.save()
        else:
            cart_item=CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
                )
            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
            cart_item.save()
        return redirect('cart')




def decrement_cart (request,prod_id,cart_item_id):
    
    product=get_object_or_404(Product,id=prod_id)
    try:
        if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
        if cart_item.quantity > 1 :
            cart_item.quantity-=1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def remove_item (request,prod_id,cart_item_id):
    product=get_object_or_404(Product,id=prod_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user,id=cart_item_id)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart (request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass
    context={
        'total':total,
        'quantity':quantity,
        'total':total,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }
    return render (request,'Store/cart.html',context)

@login_required(login_url="login")
def chekout (request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,in_active=True)
        else:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,in_active=True)
        for cart_item in cart_items:
            total+=(cart_item.product.price * cart_item.quantity)
            # quantity+=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist :
        pass
    context={
        'total':total,
        'quantity':quantity,
        'total':total,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
        }

    return render (request,'Store/chekout.html',context)
