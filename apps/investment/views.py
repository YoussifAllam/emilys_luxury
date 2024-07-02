from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND , HTTP_201_CREATED 
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

from apps.Dresses.serializers import HomeDressesSerializer , DressesSerializer
from apps.Dresses.models import Dresses , dress_images

class Investment_Details_ViewSet(APIView):
    permission_classes= [IsAuthenticated]

    def get(self, request):
        try : 
            investments = investmenter_details.objects.get( user = request.user )
        except investmenter_details.DoesNotExist:
            return Response({'status': 'failed' , 'error': 'user not found'} , HTTP_404_NOT_FOUND)
        serializer = GetInvestmentSerializer(investments)
        return Response({'status': 'success' , 'data': serializer.data} , HTTP_200_OK)
    
    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = AddInvestmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=HTTP_201_CREATED)
        return Response({'status': 'failed', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        try:
            investment = investmenter_details.objects.get(user=request.user)
        except investmenter_details.DoesNotExist:
            return Response({'status': 'failed', 'error': 'user not found'}, status=HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = AddInvestmentSerializer(investment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success'}, status=HTTP_200_OK)
        return Response({'status': 'failed', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)

class Investment_in_Dress_ViewSet(APIView):
    permission_classes= [IsAuthenticated]

    # get investmentor dresses
    
    def get(self, request):
        investments = investmenter_dresses.objects.all()
        serializer = InvestorDressListSerializer(investments, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=HTTP_200_OK)
    
    def post(self, request):
        # Create the Dress instance
        dress_serializer = DressesSerializer(data=request.data)
        if dress_serializer.is_valid():
            dress = dress_serializer.save()

            # Create the investmenter_dresses instance
            investment_data = {
                'user': request.user.id,
                'dress': dress.id
            }
            investment_serializer = InvestorDressCreateSerializer(data=investment_data)
            if investment_serializer.is_valid():
                investment_serializer.save(user=request.user, dress=dress)
                return Response({'status': 'success',}, status=HTTP_201_CREATED)
            else:
                # If the investment creation fails, delete the created dress
                dress.delete()
                return Response({'status': 'failed', 'errors': investment_serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response({'status': 'failed', 'errors': dress_serializer.errors}, status=HTTP_400_BAD_REQUEST)