from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from .models import CustomerReviews
from .serializers import CustomerReviewsSerializer
# Create your views here.


class CustomerReviewsView(APIView):
    def get(self, request):
        reviews = CustomerReviews.objects.all()
        serializer = CustomerReviewsSerializer(reviews, many=True)
        return Response({"status": "success", "data": serializer.data}, status=HTTP_200_OK)