from django.contrib import admin
from .models import Product, Bid, Profile, Measurement, ConfirmString

# Register your models here.

admin.site.register(Product)
admin.site.register(Bid)
admin.site.register(Profile)
admin.site.register(Measurement)
admin.site.register(ConfirmString)
