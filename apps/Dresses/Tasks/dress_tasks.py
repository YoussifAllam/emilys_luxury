from django.http import HttpRequest
from ..serializers_folder import parmas_serializer
from rest_framework.status import HTTP_400_BAD_REQUEST , HTTP_200_OK
from ..db_services import selectors
from ..models import Dresses as Dresses_model
from apps.investment.models import  investmenter_dresses



def check_if_request_user_is_dress_owner(request :HttpRequest , dress : Dresses_model):
    user = request.user
    investmenter_dresses_object = selectors.get_investmenter_dresses_object(dress , user)
    if not investmenter_dresses_object:
        return False
    else : 
        return True

def is_there_booking_days_in_feture_for_this_dress(request :HttpRequest , dress : Dresses_model):
    pass

def delete_dress(request :HttpRequest):
    serializer = parmas_serializer.dress_params_serializer(data=request.GET)
    
    if not serializer.is_valid():
        return ({ 'status': 'error','data' : serializer.errors}, HTTP_400_BAD_REQUEST)
    validted_data = serializer.data
    dress_uuid = validted_data.get('dress_uuid')

    dress  = selectors.get_dress_by_id(dress_uuid)
    if not dress:
        return ({ 'status': 'error','data' : 'dress not found'}, HTTP_400_BAD_REQUEST)
    
    if not check_if_request_user_is_dress_owner(request , dress):
        return ({ 'status': 'error','data' : 'you are not the owner of this dress'}, HTTP_400_BAD_REQUEST)
    
    if not is_there_booking_days_in_feture_for_this_dress(dress):
        dress.status = 'unavailable'
        return ({ 'status': 'error','data' : 'the dress have booking days in feture so we convert it to unavailable untill the booking days are over'}, HTTP_200_OK)

    dress.delete()
    
    
