# from curses.ascii import NAK
from unicodedata import category
from django.db import models
from user_app.models import Account



# Create your models here.

# class Manager(models.Model):

#     user=models.OneToOneField(Account,on_delete=models.CASCADE)


class Restuarant(models.Model):
    # manager=models.ForeignKey(Manager,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=100,null=True)
    location=models.CharField(max_length=255,null=True)

   
class Category(models.Model):
    category_name=models.CharField(max_length=50,unique=True)
    description=models.TextField(max_length=200,blank=True)


    def __str__(self):
        return self.category_name
 

class Dish(models.Model):
    dish_name=models.CharField(max_length=50,unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    image=models.ImageField()
    description=models.TextField(max_length=500,blank=True)
    price=models.IntegerField()
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return self.dish_name


class Menu(models.Model):
    dish=models.ForeignKey(Dish,on_delete=models.CASCADE)
    restuarant=models.ForeignKey(Restuarant,on_delete=models.CASCADE)

