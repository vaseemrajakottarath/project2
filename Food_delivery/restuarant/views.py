from urllib import request
from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework.response import Response
from user_app.models import Account
from.serializers import CategorySerializer, DishSerializer, RestuarantSerializer
from rest_framework import status,exceptions

from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework import generics
from rest_framework.views import APIView

from .models import Category, Dish, Restuarant

# Create your views here.


class RestuarantView(generics.CreateAPIView):

     permission_classes=[IsAdminUser]


     def get(self, request):
        restuarant = Restuarant.objects.all()
        serializer_class =RestuarantSerializer(restuarant, many=True)
        return Response(serializer_class.data)


     def post(self,request):
        
        serializer_class=RestuarantSerializer(data=request.data)

        if serializer_class.is_valid():
            serializer_class.save()
            return Response({
                "user": serializer_class.data,
                "message": "Registered Successfully"
            })
        else:
            return Response({
                "error": serializer_class.errors
            })

     def put(self,request,restuarant_id):
         
            restuarant=Restuarant.objects.get(id=restuarant_id)
            print(restuarant_id)
            serializer=RestuarantSerializer(restuarant,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message':'restuarant updated successfully'})
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
     def delete(self,request,restuarant_id):

            try:
                restuarant=Restuarant.objects.get(id=restuarant_id)
                restuarant.delete()
                return Response({'message':'Restuarant deleted successfully'})
            except restuarant.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

class CategoryView(generics.CreateAPIView):
    permission_classes=[IsAdminUser]

    def post(self,request):
        serializer_class=CategorySerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'message':"Category added successfully"})
        return Response(
            {"error":serializer_class.errors}
        )



class DishView(generics.CreateAPIView):

    permission_class=[IsAdminUser]
   
    def post(self,request,category_id):
        try:
            category=Category.objects.get(id=category_id)
            serialized_class=DishSerializer(data=request.data)
            if serialized_class.is_valid(raise_exception=True):
                serialized_class.save(category=category)
                return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
     

    def get(self,request):

        dish=Dish.objects.all()
        serializer_class=DishSerializer(dish,many=True)
        return Response(serializer_class.data)

    

    def put(self,request,dish_id):
        try:
            dish=Dish.objects.get(id=dish_id)
            serialized_class=DishSerializer(dish,data=request.data)
            if serialized_class.is_valid():
                 serialized_class.save()
                 return Response({'message':"success"})
        except exceptions.ValidationError as e:
            return Response(status=e.status_code)
        except Restuarant.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,dish_id):
        try:
            dish=Dish.objects.get(id=dish_id)
            dish.delete()
            return Response({"message":"dish deleted"})
        except Dish.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class MenuView(generics.CreateAPIView):
    def post(self,request,restuarant_id):
        restuarant=Restuarant.objects.get(id=restuarant_id)
        





        #  try:
        #     restuarant = Restuarant.objects.get(id=restuarant_id)
        #     serialized_data = self.serializer_class(instance=restuarant, data=request.data, partial=True)

        #     if serialized_data.is_valid(raise_exception=True):
        #         serialized_data.save()
        #         return Response(status=status.HTTP_200_OK)
        #  except exceptions.ValidationError as e:
        #     return Response(status=e.status_code)
        #  except Restuarant.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)


        # try:
        #     # manager=Account.objects.get(user__id=request.user.id)
        #     serialized_data=self.serializer_class(data=request.data)
        #     if serialized_data.is_valid(raise_exception=True):
        #         serialized_data.save()
        #         return Response(status=status.HTTP_200_OK)

        # except exceptions.ValidationError as e:
        #     return Response(status=e.status_code)
        # except Account.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)