from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK # , HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated



from ..serializers import  Investor_OutputSerializers 
# from ..Tasks import orders_tasks
from ..db_services import selectors

class Get_investor_dresses(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        Response_data , Response_Status = selectors.get_investor_dresses(request)
        if Response_Status != HTTP_200_OK:
            return Response(Response_data, Response_Status)
        
        investor_dress = Response_data
        Serializers = Investor_OutputSerializers.InvestorDressesSerializer(investor_dress, many=True)

        return Response({'status': 'success' , 'data' :  Serializers.data}, HTTP_200_OK)
        
class Get_investor_balance(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        Response_data , Response_Status = selectors.get_investor_balance(request)
        if Response_Status != HTTP_200_OK:
            return Response(Response_data, Response_Status)
        
        # total_balance = Response_data['total_balance']
        # curr_balance = Response_data['curr_balance']
        balance = Response_data['balance']
        Serializers = Investor_OutputSerializers.InvestorBalanceSerializer(balance)

        return Response({'status': 'success' , 'data' :  Serializers.data}, HTTP_200_OK)






