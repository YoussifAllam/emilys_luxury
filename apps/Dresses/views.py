from rest_framework.views import APIView
from .models import *
from .models import favorite_dresses as favorite_dresses_model
from .serializers_folder.serializers import *
from .Tasks.services import *
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .Tasks import dress_tasks
from django.utils.timezone import now

User = get_user_model()


class DressViewSet(APIView):

    def get(self, request, format=None):
        if not (request.user and request.user.is_authenticated):
            dresses = Dresses.objects.filter(is_approved=True)
            response_data = pagenator(dresses, request, "HomeDressesSerializer")
            return Response(response_data, status=HTTP_200_OK)
        else:
            # Fetch all approved dresses for authenticated users
            all_dresses = Dresses.objects.filter(is_approved=True)
            response_data = pagenator(
                all_dresses, request, "HomeWithFavDressesSerializer"
            )

        return Response(response_data, status=HTTP_200_OK)

    def delete(self, request):
        Response_data, Response_status = dress_tasks.delete_dress(request)
        return Response(Response_data, status=Response_status)


@api_view(["GET"])
def get_dress_using_id(request):
    uuid = request.GET.get("uuid")
    if not uuid:
        return Response(
            {"status": "error", "data": "uuid is required"}, status=HTTP_400_BAD_REQUEST
        )

    dress = Dresses.objects.get(id=uuid)
    serializer = DressesSerializer(dress, many=False, context={"request": request})

    target_dress_n_vistors, created = dress_number_of_visitors.objects.get_or_create(
        dress=dress, defaults={"number_of_visitors": 0}
    )
    n_of_vistors_serializer = number_of_visitors_Serializer(target_dress_n_vistors)

    response_data = serializer.data
    response_data["num_of_vistors"] = n_of_vistors_serializer.data
    increment_dress_number_of_visitors(
        dress_target_dress_n_vistors_instance=target_dress_n_vistors
    )
    return Response({"status": "success", "data": response_data}, status=HTTP_200_OK)


@api_view(["GET"])
def Get_product_Ratings_by_id(request):
    dress_id = request.GET.get("uuid")
    if not dress_id:
        return Response({"detail": "uuid is required."}, status=HTTP_400_BAD_REQUEST)

    ratings = dress_reviews.objects.filter(dress=dress_id)
    if not ratings.exists():
        return Response(
            {"detail": "Ratings not found for the given uuid."},
            status=HTTP_404_NOT_FOUND,
        )

    serializer = Dress_Reviews_Serializer(ratings, many=True)
    return Response({"status": "success", "data": serializer.data}, status=HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_dress_rate(request):
    product_id = request.data.get("dress_uuid")
    if not product_id:
        return Response({"detail": "uuid is required."}, status=HTTP_400_BAD_REQUEST)

    try:
        target_product = Dresses.objects.get(id=product_id)
    except Dresses.DoesNotExist:
        return Response({"detail": "Product not found."}, status=HTTP_404_NOT_FOUND)

    target_user = request.user  # Assuming your User model has a 'name' field

    target_data = {
        "dress": target_product.id,
        "Rating_stars": request.data.get("Rating_stars"),
        "user": target_user.id,  # Adjusted to standard User model field
        "feedback": request.data.get("rate_content"),
    }

    serializer = Dress_Reviews_Serializer(data=target_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)
    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_special_dress(request):
    dress = Dresses.objects.filter(is_approved=True, is_special=True)
    serializer = HomeDressesSerializer(dress, many=True)
    response_data = serializer.data
    return Response({"status": "success", "data": response_data}, status=HTTP_200_OK)


@api_view(["GET"])
def Filter_Products(request):
    Target_products = Dresses.objects.filter(is_approved=True)

    num_of_Stars = request.GET.get("num_of_Stars")
    price_from = request.GET.get("price_from")
    price_to = request.GET.get("price_to")
    measurement = request.GET.get("measurement")
    designer_name = request.GET.get("designer_name")
    Color = request.GET.get("color")
    product_type = request.GET.get("product_type")
    will_sort = request.GET.get("sort?")

    if (
        not num_of_Stars
        and not price_from
        and not price_to
        and not measurement
        and not will_sort
        and not designer_name
        and not Color
        and not product_type
    ):
        return Response({"detail": "No filter applied."}, status=HTTP_400_BAD_REQUEST)

    if product_type and (product_type != "Dress" and product_type != "Bag"):
        return Response(
            {"detail": "Invalid product type you can enter 'Dress' or 'Bag'."},
            status=HTTP_400_BAD_REQUEST,
        )

    Target_products = filter_service(
        num_of_Stars,
        price_from,
        price_to,
        measurement,
        designer_name,
        Color,
        will_sort,
        Target_products,
        request,
        product_type,
    )

    response_data = pagenator(Target_products, request, "HomeDressesSerializer")
    return Response(response_data, status=HTTP_200_OK)


@api_view(["GET"])
def get_sidebar_data(request):
    slide_data = get_slide_data(request)
    return Response({"status": "success", "data": slide_data.data}, status=HTTP_200_OK)


class favorite_dresses(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favorite_dresses_instances = favorite_dresses_model.objects.filter(
            user=user
        ).select_related("dress")
        dresses = [fav.dress for fav in favorite_dresses_instances]
        serializer = HomeDressesSerializer(dresses, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=HTTP_200_OK
        )

    def post(self, request):
        dress_uuid = request.data.get("dress_uuid")
        if not dress_uuid:
            return Response(
                {"detail": "dress_uuid is required."}, status=HTTP_400_BAD_REQUEST
            )

        try:
            target_dress = Dresses.objects.get(id=dress_uuid)
        except Dresses.DoesNotExist:
            return Response({"detail": "Product not found."}, status=HTTP_404_NOT_FOUND)
        target_data = {"dress": dress_uuid, "user": request.user.id}

        serializer = FavoriteDressSerializer(data=target_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success"}, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request):
        dress_uuid = request.data.get("dress_uuid")
        if not dress_uuid:
            return Response(
                {"detail": "dress_uuid is required."}, status=HTTP_400_BAD_REQUEST
            )
        try:
            target_dress = Dresses.objects.get(id=dress_uuid)
        except Dresses.DoesNotExist:
            return Response({"detail": "Product not found."}, status=HTTP_404_NOT_FOUND)

        try:
            favorite_dresses_obj = favorite_dresses_model.objects.get(
                dress=target_dress, user=request.user
            )
            favorite_dresses_obj.delete()
            return Response({"status": "success"}, status=HTTP_200_OK)
        except favorite_dresses_model.DoesNotExist:
            return Response(
                {"detail": "this dress not found in user favorites."},
                status=HTTP_404_NOT_FOUND,
            )


class Dress_busy_days(APIView):
    def get(self, request):
        Serializer = Dress_Params_Serializer(data=request.GET)
        if not Serializer.is_valid():
            return Response(
                {"status": "error", "data": Serializer.errors},
                status=HTTP_400_BAD_REQUEST,
            )

        dress_id = Serializer.data.get("uuid")
        try:
            target_dress = Dresses.objects.get(id=dress_id)
        except Dresses.DoesNotExist:
            return Response({"detail": "Product not found."}, status=HTTP_404_NOT_FOUND)

        busy_days = dress_busy_days.objects.filter(
            dress=target_dress, busy_day__gte=now().date()
        )
        s = Busy_days_Serializer(busy_days, many=True)
        return Response({"status": "success", "data": s.data}, status=HTTP_200_OK)


# from django.utils import timezone
# from apps.Dresses.models import dress_busy_days
# from datetime import timedelta , datetime

# @api_view(['GET'])
# def Test_busy_days(request):
#     expiration_time = timezone.now() - timedelta(minutes=1)  # Adjust this duration as needed
#     # busy_days = dress_busy_days.objects.filter(is_temporary=True, created_at__lt=expiration_time)
#     busy_days = dress_busy_days.objects.all()
#     s = Busy_days_Serializer(busy_days, many=True)

#     return Response({ 'status': 'success','data' : s.data}, status=HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)
from django.core.mail import send_mail


class ValidateTokenView(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        print("=======================", request.headers)
        logger.info(f"User: {request.user}")
        logger.info(f"Authorization Header: {request.headers.get('Authorization')}")
        body = "Your password reset link is : {}".format(request.headers)
        send_mail(
            "Paswword reset from Baggr",
            body,
            "Baggr@gmail.com",  # TODO: Replace with your email __________________________________________________
            ["youssifhassan011@gmail.com"],
        )
        return Response({"detail": "Token is valid"}, status=HTTP_200_OK)
