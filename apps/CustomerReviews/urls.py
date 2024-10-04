from django.urls import path
from .views import *

urlpatterns = [
    path("CustomerReviews/", CustomerReviewsView.as_view(), name="customer-reviews"),
]
