from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OutputSerializers
from .db_services import selectors
from rest_framework.permissions import IsAuthenticated
from .Tasks import trade_tasks


class user_points(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_points = selectors.get_user_points(request.user)
        serializer = OutputSerializers.UserPointsSerializers(user_points)
        return Response({"status": "success", "data": serializer.data}, HTTP_200_OK)


class Trade_points(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        Response_data, Response_status = trade_tasks.Trade_points(request)
        return Response(Response_data, Response_status)
