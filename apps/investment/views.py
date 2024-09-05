from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response 
from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST , HTTP_404_NOT_FOUND , HTTP_201_CREATED 
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
User = get_user_model()

from apps.Dresses.serializers_folder.serializers import DressesSerializer
# from apps.Dresses.models import Dresses , dress_images
from .Tasks import register_beneficiary_tasks , invest_in_dress_tasks
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
            # Response_data , beneficiary_details = register_beneficiary_tasks.Create_Wallet(data)
            if True:
                try:
                    with transaction.atomic():
                        # Store the beneficiary details in your database
                        investment = investmenter_details.objects.create(
                            user=request.user,
                            mobile=data.get('mobile'),
                            account_owner_name=data.get('account_owner_name'),
                            credit_card_number=data.get('credit_card_number'),
                            bank_name=data.get('bank_name'),
                            # payout_account_id=beneficiary_details['id'] ,
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
        is_valid = invest_in_dress_tasks.check_if_use_have_investmenter_details(request.user)
        if not is_valid:
            return Response({'status': 'failed', 'error': 'you should add your investment details first'}, status=HTTP_400_BAD_REQUEST)
        
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
                return Response({'status': 'success','dress_uuid': dress_serializer.data['id']}, status=HTTP_201_CREATED)
            else:
                # If the investment creation fails, delete the created dress
                dress.delete()
                return Response({'status': 'failed', 'errors': investment_serializer.errors}, status=HTTP_400_BAD_REQUEST)
        return Response({'status': 'failed', 'errors': dress_serializer.errors}, status=HTTP_400_BAD_REQUEST)
    
class DressPhotoUploadView(APIView):
    def post(self, request):
        # Validate that the car exists
        dress_uuid = request.data.get('dress_uuid')
        try:
            dress = Dresses.objects.get(id=dress_uuid)
        except Dresses.DoesNotExist:
            return Response({"message": "Dress not found"}, status=HTTP_404_NOT_FOUND)
        
        # Process each photo in the request
        photos = request.FILES.getlist('images')  # Assuming the photos are uploaded with the key 'photos'
        if not dress_uuid or not photos:
            return Response({"message": "Please provide dress_uuid and images"}, status=HTTP_400_BAD_REQUEST)
        # print('--------------' , photos)
        for photo in photos:
            dress_images.objects.create(dress=dress, image=photo)

        # You might want to return the URLs of the uploaded photos or just a success message
        return Response({
            "status": "success",
            "message": "Photos uploaded successfully"
            }, status=HTTP_201_CREATED)

from django.conf import settings
import base64
import requests
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_payout_account(request):
    api_key = settings.SECRET_KEY
    encoded_api_key = base64.b64encode(api_key.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_api_key}',
        'Content-Type': 'application/json',
    }
    
    
    response = requests.get(f'https://api.moyasar.com/v1/payout_accounts', headers=headers)

    
    return Response({'message': response.json()}, status=HTTP_400_BAD_REQUEST)