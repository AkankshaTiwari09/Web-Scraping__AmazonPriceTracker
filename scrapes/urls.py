from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('products', products, name='products'),
    path('confirm_delete/<prod_id>',confirm_delete,name='Confirm_delete')

]