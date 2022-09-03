from django.contrib import admin

# Register your models here.
from . models import Restuarant,Dish,Category

admin.site.register(Restuarant)
admin.site.register(Category)
admin.site.register(Dish)