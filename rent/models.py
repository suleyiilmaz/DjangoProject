from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from product.models import Product



class Rent(models.Model):
    STATUS=(
        ('New','New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
        ('Preaparing', 'Preaparing'),

    )

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    code=models.CharField(max_length=5,editable=False)
    first_name=models.CharField(max_length=10)
    last_name=models.CharField(max_length=10)
    start_date=models.DateField()
    end_date = models.DateField()
    phone=models.CharField(blank=True,max_length=20)
    address=models.CharField(blank=True,max_length=20)
    city=models.CharField(blank=True,max_length=20)
    country=models.CharField(blank=True,max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip=models.CharField(blank=True,max_length=20)
    adminnote=models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name



class RentForm(ModelForm):
    class Meta:
        model=Rent
        fields=['first_name','last_name','start_date','end_date','address','phone','city','country']

class RentProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    rent=models.ForeignKey(Rent,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title













