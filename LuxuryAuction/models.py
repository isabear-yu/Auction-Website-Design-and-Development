from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=400)
    picture = models.FileField()
    content_type = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="All")
    starting_bid = models.DecimalField(max_digits=20, decimal_places=2)
    starting_time = models.DateTimeField()
    ending_time = models.DateTimeField()
    isPaid = models.BooleanField(default=False)


class Bid(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    emailsent = models.CharField(max_length=1, default="N")


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    age = models.IntegerField()
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)


class Measurement(models.Model):
    location = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Distance from {self.location} to {self.destination} is {self.distance} km"


class ConfirmString(models.Model):
    code = models.CharField(max_length=256)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    c_time = models.DateTimeField()
    has_confirmed = models.BooleanField(default=False)

