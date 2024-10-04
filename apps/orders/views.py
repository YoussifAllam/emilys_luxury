from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.views import APIView
from .db_services import services, selectors
from .Tasks import order_tasks
from rest_framework.permissions import IsAuthenticated
from .serializers import OutputSerializers
from rest_framework.decorators import api_view, permission_classes


class Order(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data, status = selectors.get_cart(request)
        if status != HTTP_200_OK:
            return Response(data, status=status)

        total_price, Target_cart, data, status = order_tasks.Calculate_total_price(
            data, request
        )
        if status != HTTP_200_OK:
            return Response(data, status=status)

        data, status = services.create_order(request, total_price)
        if status != HTTP_201_CREATED:
            return Response(data, status=status)

        data, status = services.create_order_items(data, Target_cart)

        return Response(data, status=status)

    def get(self, request):
        # get target orer using it's uuid
        data, status = selectors.get_order_using_request(request)
        if status == HTTP_200_OK:
            order = data["Target_order"]
            serializer = OutputSerializers.GetOrderSerializer(order)
            return Response(
                {"status": "succes", "data": serializer.data}, status=HTTP_200_OK
            )
        return Response(data, status=status)

    def patch(self, request):
        data, status = services.update_order_status(request)
        return Response(data, status=status)


class OrderItems(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data, status = selectors.get_order_items(request)
        if status == HTTP_200_OK:
            order_items = data["order_items"]
            serializer = OutputSerializers.GetOrderItemSerializer(
                order_items, many=True
            )
            return Response(
                {"status": "succes", "data": serializer.data}, status=HTTP_200_OK
            )
        return Response(data, status=status)


class OrderDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        pass

    def post(self, request):
        Response_data, Response_status = selectors.get_order_using_request(request)
        if Response_status != HTTP_200_OK:
            return Response(Response_data, status=Response_status)

        Response_data, Response_status = services.create_order_detail(
            request, Response_data["Target_order"]
        )
        return Response(Response_data, status=Response_status)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    data, status = selectors.get_user_orders(request)
    if status == HTTP_200_OK:
        orders = data["orders"]
        serializer = OutputSerializers.GetOrderSerializer(orders, many=True)
        return Response(
            {"status": "succes", "data": serializer.data}, status=HTTP_200_OK
        )
    return Response(data, status=status)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def track_order(request):
    data, status = selectors.get_order_uuig_regquest_get(request)
    if status == HTTP_200_OK:
        Target_order = data["Target_order"]
        print(Target_order)
        serializer = OutputSerializers.GetOrderDetailSerializer(Target_order)
        return Response(
            {"status": "succes", "data": serializer.data}, status=HTTP_200_OK
        )
    return Response(data, status=status)


class Get_Put_order_details(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        Response_data, Response_status = order_tasks.get_order_details(request)
        return Response(Response_data, status=Response_status)

    def put(self, request):
        Response_data, Response_status = order_tasks.update_order_details(request)
        return Response(Response_data, status=Response_status)
