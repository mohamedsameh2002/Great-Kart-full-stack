
from django.urls import path
from . import views
urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:prod_id>/',views.add_cart,name='add_cart'),
    path('decrement_cart/<int:prod_id>/<int:cart_item_id>/',views.decrement_cart,name='decrement_cart'),
    path('remove_item/<int:prod_id>/<int:cart_item_id>/',views.remove_item,name='remove_item'),
    path('chekout/',views.chekout,name='chekout'),

]

