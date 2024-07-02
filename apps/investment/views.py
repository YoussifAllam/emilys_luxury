from rest_framework.views import APIView
from .models import *
from .serializers import *
# from .services import *
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND , HTTP_201_CREATED 
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

class InvestmentViewSet(APIView):
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


