from django.urls import path

from .views import food_list, forget_code, get_sessions, login, logout, reserve_food

urlpatterns = [
    path("v1/login/", login, name="login"),
    path("v1/reserve-food/", reserve_food, name="reserve-food"),
    path("v1/get-food-list/", food_list, name="get-food-list"),
    path("v1/get-forget-code/", forget_code, name="get-forget-code"),
    path("v1/logout/", logout, name="logout"),
    path("v1/get-sessions/", get_sessions, name="get-sessions"),
]
