from rest_framework.status import HTTP_200_OK  , HTTP_400_BAD_REQUEST
from django.http import HttpRequest
from ..serializers import investor_inputSerializers 
from apps.Dresses.models import Dresses

def patch_investor_dresses(request : HttpRequest , dress_instance : Dresses) -> tuple[dict, int]:
    patch_serializer = investor_inputSerializers.DressesSerializer(
        instance=dress_instance, 
        data=request.data, 
        partial=True  # Allows for partial updates
    )
    if not patch_serializer.is_valid():
        return ({'status': 'error', 'data': patch_serializer.errors}, HTTP_400_BAD_REQUEST)

    patch_serializer.save()

    return ({ 'status': 'success','data' : 'ok'}, HTTP_200_OK)
