from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,ReviewRating,ProductGallery
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage,Paginator,PageNotAnInteger
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
from .filters import ProducstFilter
# Create your views here.


def store (request,cat_slug=None):
    categorios=None
    products=None
    ATOZ=request.GET.get('ATOZ')
    ZTOA=request.GET.get('ZTOA')
        

    if cat_slug != None :
        categorios= get_object_or_404(Category,slug=cat_slug)
        products=Product.objects.filter(catefory=categorios,is_available=True).order_by('-created_date')
        filter=ProducstFilter(request.GET,queryset=products)
        products=filter.qs
        if ATOZ:
            paged_product=Product.objects.filter(is_available=True).order_by('product_name')
        elif ZTOA:
            paged_product=Product.objects.filter(is_available=True).order_by('-product_name')
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
    else:
        products=Product.objects.filter(is_available=True).order_by('-created_date')
        filter=ProducstFilter(request.GET,queryset=products)
        products=filter.qs
        if ATOZ:
            paged_product=Product.objects.filter(is_available=True).order_by('product_name')
        elif ZTOA:
            paged_product=Product.objects.filter(is_available=True).order_by('-product_name')
        paginator=Paginator(products,2)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)

        # filter

    if ATOZ:
        paged_product=Product.objects.filter(is_available=True).order_by('product_name')
    elif ZTOA:
        paged_product=Product.objects.filter(is_available=True).order_by('-product_name')
        
        

    context={
        'products':paged_product,
        'filter':filter,
    }


    return render(request,'Store/store.html',context)




def product_detail(request,cat_slug,prod_slug):
    try:
        product=Product.objects.get(catefory__slug=cat_slug,slug=prod_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product).exists()
    except Exception as e:
        raise e
    
    # chek if user ordered it before review it 
    if request.user.is_authenticated:
        try:
            orderproduct=OrderProduct.objects.filter(user=request.user,product_id=product.id).exists()
        except OrderProduct.DoesNotExist :
            orderproduct=None
    else:
        orderproduct=None

    # get th reivews
    reviews=ReviewRating.objects.filter(product__id=product.id,status=True)
    product_gallery=ProductGallery.objects.filter(product__id=product.id)# re seee

    context={
    'product':product,
    'in_cart':in_cart,
    'orderproduct':orderproduct,
    'reviews':reviews,
    'product_gallery':product_gallery,
    }
    return render (request,'Store/product_detail.html',context)





def search (request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword)) 
    context={'products':products}
    return render (request,'Store/store.html',context)





def submet_review (request,prod_id):
    url=request.META.get('HTTP_REFERER')#==========================================================
    if request.method == 'POST':
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=prod_id)
            form=ReviewForm(request.POST,instance=reviews)
            form.save()
            messages.success(request,'thank you , your review has been updeted')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.rating=form.cleaned_data['rating']
                data.review=form.cleaned_data['review']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=prod_id #       الاندرسكور هنا معناها (اللي)
                data.user_id=request.user.id
                data.profile_id=3
                # data.user_profile_user=request.user
                # print(data.user_profile_user)
                data.save()
                messages.success(request,'thank you , your review has been submeted')
                return redirect(url)