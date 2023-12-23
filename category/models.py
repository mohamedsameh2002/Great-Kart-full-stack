from django.db import models
from django.shortcuts import redirect
from django.urls import reverse


# Create your models here.

class Category (models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    slug=models.SlugField(max_length=100,unique=True)
    description=models.TextField(max_length=250,blank=True)
    cat_image=models.ImageField(upload_to='photos/categoryies',blank=True)
    class Meta:
        verbose_name_plural='Category'
    def __str__(self):
        return self.category_name
    
    def get_url (self):
        return reverse ('product_by_catigory',args=[self.slug])
    