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
from .Tasks import register_beneficiary_tasks
import logging
from django.db import transaction

logger = logging.getLogger(__name__)

class Investment_Details_ViewSet(APIView):
    permission_classes= [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = AddInvestmentSerializer(data=data)
        
        if serializer.is_valid():
            # Register the beneficiary account with Moyasar
            Response_data , beneficiary_details = register_beneficiary_tasks.Create_Wallet(data)
            if beneficiary_details:
                try:
                    with transaction.atomic():
                        # Store the beneficiary details in your database
                        investment = investmenter_details.objects.create(
                            user=request.user,
                            mobile=data.get('mobile'),
                            account_owner_name=data.get('account_owner_name'),
                            # credit_card_number=data.get('credit_card_number'),
                            # bank_name=data.get('bank_name'),
                            payout_account_id=beneficiary_details['id'] ,
                            # iban=data.get('iban') 
                        )
                        
                        return Response({'status': 'success', 'message': 'User registered successfully'}, status=HTTP_201_CREATED)
                except Exception as e:
                    logger.error(f"Error occurred during transaction: {e}")
                    return Response({'status': 'failed', 'error': 'Failed to register beneficiary account'}, status=HTTP_400_BAD_REQUEST)
            else:
                logger.error("Failed to register beneficiary account")
                return Response({'status': 'failed', 'error': 'Failed to register beneficiary account' , 
                                 'data': Response_data}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'status': 'failed', 'data': serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        try : 
            investments = investmenter_details.objects.get( user = request.user )
        except investmenter_details.DoesNotExist:
            return Response({'status': 'failed' , 'error': 'user not found'} , HTTP_404_NOT_FOUND)
        serializer = GetInvestmentSerializer(investments)
        return Response({'status': 'success' , 'data': serializer.data} , HTTP_200_OK)
    
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
    

from django.conf import settings
import base64
import requests
from rest_framework.decorators import api_view

@api_view(['DELETE'])
def get_payout_account(request):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }
    
    account_id = request.GET.get('id')
    if not account_id:
        return Response({'error': 'Payout account ID is required'}, status=HTTP_400_BAD_REQUEST)
    
    logger.debug(f"Attempting to delete payout account with ID: {account_id}")
    
    response = requests.delete(f'https://api.moyasar.com/v1/payout_accounts/{account_id}', headers=headers)

    if response.status_code == 204:
        logger.info(f"Successfully deleted payout account with ID: {account_id}")
        return Response({'message': 'Payout account deleted successfully'}, status=HTTP_400_BAD_REQUEST)
    else:
        logger.error(f"Failed to delete payout account: {response.json()}")
        return Response(response.json(), status=response.status_code)