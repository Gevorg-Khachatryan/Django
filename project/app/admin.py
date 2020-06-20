from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Users)
admin.site.register(Products_photos)
admin.site.register(Products)
admin.site.register(Messages)
admin.site.register(Basket)

