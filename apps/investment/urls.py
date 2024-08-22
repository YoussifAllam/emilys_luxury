from django.urls import path
from . views import *

urlpatterns = [

    path('InvestmentViewSet/', Investment_Details_ViewSet.as_view(), name='investment'), 
    path('Investment_in_Dress_ViewSet/' , Investment_in_Dress_ViewSet.as_view(),) , 
    path('upload_dress_images/' , DressPhotoUploadView.as_view())


    ,path('get_payout_accounts/' , get_payout_account)
]