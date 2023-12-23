

from django.urls import path
from . import views
from django.conf import settings
urlpatterns = [
    path('',views.store,name='store'),
    path('category/<str:cat_slug>/',views.store,name='product_by_catigory'),
    path('category/<str:cat_slug>/<str:prod_slug>/',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('submet_review/<int:prod_id>/',views.submet_review,name='submet_review'),
]

