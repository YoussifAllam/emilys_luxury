from django.urls import path
from . import views

urlpatterns = [

    path('InvestmentViewSet/', views.InvestmentViewSet.as_view(), name='investment'),   

]