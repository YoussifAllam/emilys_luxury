from django.urls import path , include

urls_for_investor = [

]

urls_for_Renter = [

]



urlpatterns = [
    path('investor/', include(urls_for_investor)),
    
    path('renter/', include(urls_for_Renter)),

]