import django_filters
from .models import Product

class ProducstFilter(django_filters.FilterSet):
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    class Meta:
        model = Product
        
        fields = [
            'price__gt',
            'price__lt',
            
        ]
