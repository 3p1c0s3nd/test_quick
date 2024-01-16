from django.contrib import admin
from .models import BillProduct, Bill, Client, Product
# Register your models here.

admin.site.register([ BillProduct, Bill, Client, Product ])
