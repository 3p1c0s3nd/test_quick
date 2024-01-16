from django.db import models


# Create your models here.
class Client(models.Model):
    def is_authenticated(self):
        return True  # Always consider authenticated
    
    document = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Bill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    nit = models.CharField(max_length=15)
    code = models.CharField(max_length=20)


class BillProduct(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
