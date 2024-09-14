from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK # , HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated


from apps.orders.models import Order
from apps.invitation.models import user_invitation_points
from apps.Dresses.models import favorite_dresses

from ..serializers import  OutputSerializers
# from ..Tasks import orders_tasks
from ..db_services import selectors
from .. import constants

class Get_renter_orders(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self , request):
        user = request.user
        orders = Order.objects.filter(user=user )
        serializer = OutputSerializers.GetOrderSerializer(orders , many=True)
        return Response({ 'status' : 'success' , 'data' : serializer.data } , status=HTTP_200_OK)
    
class Get_user_num_of_points_and_code(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user_Data, created = user_invitation_points.objects.get_or_create(user=request.user)
        serializer = OutputSerializers.UserPointsSerializers(user_Data)
        serializer_data = serializer.data
        user_code = serializer_data['user_code']

        url =  constants.url

        return Response({'status': 'success', 'data': {
            'num_of_points': serializer_data['num_of_points'],
            'invite_url': f'{url}?invitation={user_code}'

        }}, status=HTTP_200_OK)
    
class Get_favorite_dresses(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        dresses = favorite_dresses.objects.filter(user=request.user)
        serializer = OutputSerializers.FavDressesListSerializer(dresses, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=HTTP_200_OK)

class GetOrderShippingAddress(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        order_details, status_code = selectors.get_user_orders_details(request)
        if status_code != HTTP_200_OK:
            return Response({'status': 'failed', 'data': 'no orders address'}, status=status_code)
        
        serializer = OutputSerializers.ShippingAddressSerializer(order_details, many=True)
        return Response({'status': 'success', 'data': serializer.data}, status=HTTP_200_OK)



