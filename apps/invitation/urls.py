from django.urls import path
from .views import *


urlpatterns = [
    path('get_user_points/' , user_points.as_view()) , 
    path('Trade_points/' , Trade_points.as_view())
]