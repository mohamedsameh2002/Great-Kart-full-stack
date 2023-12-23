from django.contrib import admin
from .models import *
import admin_thumbnails
# Register your models here.

@admin_thumbnails.thumbnail('img')
class ProductGalleryInline (admin.TabularInline) :
    model=ProductGallery
    extra=1


class ProductAdmin (admin.ModelAdmin):
    list_display=['product_name','price','stock','catefory','modified_date','is_available']
    prepopulated_fields={'slug':('product_name',)}
    inlines=[ProductGalleryInline]

class VariationAdmin (admin.ModelAdmin):
    list_display=['product','variation_category','variation_value','is_acctive','created_date']
    list_editable=['is_acctive']
    list_filter=['product','variation_category','variation_value','is_acctive']


admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)