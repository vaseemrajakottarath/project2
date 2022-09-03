from .models import Category, Dish, Restuarant
from rest_framework import serializers


class RestuarantSerializer(serializers.ModelSerializer):
    class Meta:
        model=Restuarant
        fields=('name','address','location')

        def create(self,validated_data):
            restuarant=Restuarant.objects.create(**validated_data)
            restuarant.save()
            return restuarant


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=('category_name','description')

        def create(self,validated_data):
            category=Category.objects.create(**validated_data)
            category.save()
            return category



class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dish
        fields=('dish_name','description','price')
    
    def create(self,validated_data):
        dish=Dish.objects.create(**validated_data)
        dish.save()
        return dish



    def to_representation(self, instance):
        return {
            'category':instance.category.category_name
        }

        