from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegistrationForm,UserForm,UserProfileForm
from.models import Accounts,UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from cart.models import Cart,CartItem
from cart.views import _cart_id
import requests
from orders.models import Order,OrderProduct

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.

def register (request):
    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_numper=form.cleaned_data['phone_numper']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Accounts.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_numper=phone_numper
            user.save()

            # user acctvation
            current_site=get_current_site(request)
            mail_supject='pleass activate your account.'
            message=render_to_string('Accounts/verification_email.html',{
                'user':user,
                'domin':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email 
            send_email=EmailMessage(mail_supject,message,to=[to_email])
            send_email.send()
            # messages.info(request,'thank u for registrin,pleas acteave your account from th masseg')
            return redirect ('/accounts/login/?command=verification&email='+email)
    else:
        form=RegistrationForm()
    return render (request,'Accounts/register.html',{'form':form})


def activate (request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)
    except (TypeError,OverflowError,ValueError,Accounts.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        messages.success(request,'the email is acctiave success')
        return redirect('login')
    else:
        messages.error(request,'the email dose not  acctivate ')
        return redirect('register')

def login (request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['Password']
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exist=CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_item=CartItem.objects.filter(cart=cart)
                    #geting product variation by cart id
                    product_variation=[]
                    for item in cart_item:
                        veriation=item.variation.all()
                        product_variation.append(list(veriation))
                    # geting cart items from the user to accsess his product variation
                    cart_item=CartItem.objects.filter(user=user)
                    #existing veriation list
                    ex_ver_list=[]
                    id=[]
                    for item in cart_item:
                        existing_variation=item.variation.all()
                        ex_ver_list.append(list (existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_ver_list:
                            index=ex_ver_list.index(pr)
                            item_id=id[index]
                            item=CartItem.objects.get(id=item_id)
                            item.quantity+=1
                            item.user=user
                            item.save()
                        else:
                            cart_item=CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user=user
                                item.save()
            except:
                pass
            auth.login(request,user)
            messages.success(request,'you are logged in ')
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                parmas=dict(x.split('=')for x in query.split('&') )
                if 'next' in parmas:
                    nextPage=parmas['next']
                    return redirect(nextPage)
            except:  
                return redirect('dashboard')
        else:
            messages.error(request,'invaled login ')
            return redirect('login')
    return render (request,'Accounts/login.html')


@login_required(login_url='login')
def logout (request):
    auth.logout(request)
    messages.info(request,'log out')
    return redirect('login')



@login_required(login_url='login')
def dashboard (request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    orders=Order.objects.filter(user_id=request.user.id,is_order=True)
    orders_count=orders.count()
    return render (request,'Accounts/dashboard.html',{'orders_count':orders_count,'userprofile':userprofile})


def forgotpassword (request):
    if request.method == 'POST':
        email=request.POST['email']
        if Accounts.objects.filter(email=email).exists():
            user=Accounts.objects.get(email__exact=email)
            #reset password email
            current_site=get_current_site(request)
            mail_supject='Reset your password'
            message=render_to_string('Accounts/reset_password_email.html',{
                'user':user,
                'domin':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email 
            send_email_pass=EmailMessage(mail_supject,message,to=[to_email])
            send_email_pass.send()
            messages.success(request,'password reset email has been sent to your email')
            return redirect('forgotpassword')
        else:
            messages.error(request,'account is not exists')

    return render (request,'Accounts/forgotpassword.html')

# link validate password on gmail redirect in thes method
def resetpassword_validate (request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Accounts._default_manager.get(pk=uid)
    except (TypeError,OverflowError,ValueError,Accounts.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'pleas reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'thes link has been expierd')
        return redirect('login')


def resetpassword (request):
    if request.method == 'POST':
        password=request.POST['Password']
        conf_password=request.POST['Confirm_Password']
        if password == conf_password:
            if len(password) < 6:
                messages.error(request,'Please enter a password containing at least 6 elements')
                return redirect('resetpassword')
            else :
                uid=request.session.get('uid')
                user=Accounts.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request,'password reseted succsessful')
                return redirect('login')
        else:
            messages.warning(request,'password dont match')
            return redirect('resetpassword')
    else:
        return render (request,'Accounts/resetpassword.html')
    

@login_required(login_url='login')
def my_orders (request):
    orders=Order.objects.filter(user_id=request.user.id,is_order=True).order_by('-created_at')
    return render (request,'Accounts/my_orders.html',{'orders':orders})

@login_required(login_url='login')
def edit_profile (request):
    userprofile=get_object_or_404(UserProfile,user=request.user)
    if request.method == 'POST':
        user_form=UserForm(request.POST,instance=request.user)
        profile_form=UserProfileForm(request.POST,request.FILES,instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'your profile has been updeted')
            return redirect('edit_profile')
    else:
        user_form=UserForm(instance=request.user)
        profile_form=UserProfileForm(instance=userprofile)
    context={
    'profile_form':profile_form,
    'user_form':user_form,
    'userprofile':userprofile,
    }
    return render(request,'Accounts/edit_profile.html',context)

@login_required(login_url='login')
def changePassword (request):
    if request.method == 'POST':
        old_password=request.POST['old_password']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']
        user=Accounts.objects.get(username__exact=request.user.username)
        if new_password == confirm_password :
            success=user.check_password(old_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password Has Been Changed Successfuly')
                return redirect('changePassword')
            else:
                messages.error(request,'The Old Password Is Not Correct')
                return redirect('changePassword')
        else:
            messages.error(request,'Two passwords do not match')
            return redirect('changePassword')

    return render(request,'Accounts/changePassword.html')


@login_required(login_url='login')
def order_detail (request,order_number):
    order_detail=OrderProduct.objects.filter(order__order_numper=order_number)
    order=Order.objects.get(order_numper=order_number)
    subtotal=0
    for i in order_detail:
        subtotal+= i.product_price * i.quantity

    context={
        'order_detail':order_detail,
        'order':order,
        'subtotal':subtotal,
    }
    return render(request,'Accounts/order_detail.html',context)