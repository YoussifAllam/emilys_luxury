from django.urls import path, include
from .views import Rentner_views, investor_views

urls_for_investor = [
    path("Get_investor_dresses/", investor_views.investor_dresses.as_view()),
    path("Get_investor_balance/", investor_views.Get_investor_balance.as_view()),
    path("upload_dress_images/", investor_views.DressPhotoUploadView.as_view()),
]

urls_for_Renter = [
    path("get_user_orders/", Rentner_views.Get_renter_orders.as_view()),
    path(
        "Get_user_num_of_points/",
        Rentner_views.Get_user_num_of_points_and_code.as_view(),
    ),
    path("Get_favorite_dresses/", Rentner_views.Get_favorite_dresses.as_view()),
    path(
        "Get_order_shipping_address/", Rentner_views.GetOrderShippingAddress.as_view()
    ),
]


urlpatterns = [
    path("investor/", include(urls_for_investor)),
    path("renter/", include(urls_for_Renter)),
]
