from django.urls import path

from .views import food_list, forget_code, get_sessions, login, logout, reserve_food

app_name = "boostan_api"
urlpatterns = [
    path("login/", login, name="login"),
    path("reserve-food/", reserve_food, name="reserve-food"),
    path("get-food-list/", food_list, name="get-food-list"),
    path("get-forget-code/", forget_code, name="get-forget-code"),
    path("logout/", logout, name="logout"),
    path("get-sessions/", get_sessions, name="get-sessions"),
]
