from django.shortcuts import render,redirect
from store.models import Product,ReviewRating


def home (request):
    products=Product.objects.filter(is_available=True).order_by('-created_date')
    for product in products:
        reviews=ReviewRating.objects.filter(product__id=product.id,status=True)
    
    context={'products':products,'reviews':reviews}
    return render(request,'home.html',context)