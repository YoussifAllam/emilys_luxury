from .views import *
from django.urls import path


urlpatterns = [
    path("dresses/", DressViewSet.as_view(), name="dresses"),
    path("get_dress_using_id/", get_dress_using_id),
    path("Get_product_Ratings_by_id/", Get_product_Ratings_by_id),
    path("add_dress_rate/", add_dress_rate),
    path("get_special_dress/", get_special_dress),
    path("Filter_Products/", Filter_Products),
    path("get_sidebar_data/", get_sidebar_data),
    path("favorite_dresses/", favorite_dresses.as_view(), name="favorite_dresses"),
    path("validate-token/", ValidateTokenView.as_view(), name="validate-token"),
    path("get_dress_BasyDays/", Dress_busy_days.as_view()),
    # path('test/' , Test_busy_days)
]
