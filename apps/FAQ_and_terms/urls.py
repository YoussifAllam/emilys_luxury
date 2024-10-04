from django.urls import path, include
from .views import *

urlpatterns = [
    path("GET_ALL_FAQ/", Get_FAQ),
    path("Get_terms_and_condations/", Get_terms_and_condations),
]
