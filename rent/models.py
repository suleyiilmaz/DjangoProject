from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm

from product.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.product

    @property
    def amount(self):
        return ((self.end_date - self.start_date) * self.product.price)

    @property
    def price(self):
        return (self.product.price)


class Rent(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
        ('Preaparing', 'Preaparing'),

    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(max_length=5, editable=False, blank=True)
    first_name = models.CharField(max_length=10, blank=True)
    last_name = models.CharField(max_length=10, blank=True)

    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=20)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField(blank=True, max_length=10, default="0")
    status = models.CharField(max_length=10, choices=STATUS, default='New', blank=True)
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['start_date', 'end_date']


class RentForm(ModelForm):
    class Meta:
        model = Rent
        fields = ['first_name', 'last_name', 'address', 'phone', 'city', 'country']


class RentProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True, auto_now=True)
    end_date = models.DateField(blank=True, auto_now=True)
    price = models.FloatField(default="0")
    amount = models.FloatField(default="0")
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
