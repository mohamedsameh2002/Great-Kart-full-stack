from django.db import models
from category.models import Category
from accounts.models import Accounts
from django.db.models import Avg,Count
from accounts.models import UserProfile
# Create your models here.


class Product (models.Model):
    product_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    catefory = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    def averageReview (self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg=float(reviews['average'])
        return avg
    def countReview (self):
        reviews=ReviewRating.objects.filter(product=self,status=True).aggregate(count=Count('id'))
        cont =0
        if reviews['count'] is not None:
            cont=int(reviews['count'])
        return cont



class VariationManager (models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_acctive=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_acctive=True)


VIRIATION_CAT = [
    ('color', 'color'),
    ('size', 'size'),]


class Variation (models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(
        max_length=100, choices=VIRIATION_CAT)
    variation_value = models.CharField(max_length=100)
    is_acctive = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.variation_value)


class ReviewRating (models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject

class ProductGallery (models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,default=None)
    img=models.ImageField(upload_to='store/products')
    def __str__(self) -> str:
        return self.product.product_name
    class Meta:
        verbose_name= 'ProductGallery'
        verbose_name_plural= 'ProductGallery'