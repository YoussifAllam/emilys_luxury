from rest_framework.status import HTTP_200_OK , HTTP_201_CREATED ,HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.views import APIView
# from .models import Payment
from .serializers import InputSerializers , OutputSerializers
# from .Tasks import order_tasks
from .db_services import selectors
from rest_framework.permissions import IsAuthenticated


class user_points(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user_points = selectors.get_user_points(request.user)
        serializer = OutputSerializers.UserPointsSerializers(user_points)
        return Response({'status':'success' , 
             'data':serializer.data } , HTTP_200_OK)


