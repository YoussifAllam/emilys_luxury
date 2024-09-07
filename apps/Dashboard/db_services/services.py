from rest_framework.status import HTTP_200_OK  , HTTP_404_NOT_FOUND , HTTP_400_BAD_REQUEST
from django.http import HttpRequest
from ..serializers import investor_inputSerializers , params_serializer
from ..db_services import selectors


def patch_investor_dresses(request : HttpRequest) -> tuple[dict, int]:
    serializer = params_serializer.DressParamsSerializer(data=request.GET)
    if not serializer.is_valid():
        return ({ 'status': 'error','data' : serializer.errors}, HTTP_400_BAD_REQUEST)
    
    dress_id = serializer.validated_data.get('dress_id')
    dress_instance = selectors.get_dress_using_uuid(dress_id)
    if not dress_instance: return ({ 'status': 'error','data' : 'dress not found'}, HTTP_404_NOT_FOUND)
    print('_____________' , request.data)
    patch_serializer = investor_inputSerializers.DressesSerializer(
        instance=dress_instance, 
        data=request.data, 
        partial=True  # Allows for partial updates
    )
    if not patch_serializer.is_valid():
        return ({'status': 'error', 'data': patch_serializer.errors}, HTTP_400_BAD_REQUEST)

    patch_serializer.save()

    return ({ 'status': 'success','data' : 'ok'}, HTTP_200_OK)

