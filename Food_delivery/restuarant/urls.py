from django import views
from django.urls import path
from .views import RestuarantView,DishView,CategoryView


urlpatterns=[
    path('add/restuarant',RestuarantView.as_view()),
    path('update/restuarant/<int:restuarant_id>',RestuarantView.as_view()),
    path('delete/restuarant/<int:restuarant_id>',RestuarantView.as_view()),

    path('add/category',CategoryView.as_view()),
    path('dishes/',DishView.as_view()),
    path('add/dish/<int:category_id>', DishView.as_view()),
    path('update/dish/<int:dish_id>',DishView.as_view()),
    path('delete/dish/<int:dish_id>',DishView.as_view()),
    # path('menu')        
]