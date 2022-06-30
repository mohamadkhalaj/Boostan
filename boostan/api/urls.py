from django.urls import path

from .views import food_list, reserve_food

urlpatterns = [
    path("v1/reserve-food/", reserve_food, name="reserve-food"),
    path("v1/get-food-list/", food_list, name="get-food-list"),
]
