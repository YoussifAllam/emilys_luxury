from django.http import HttpRequest
from ..serializers_folder import parmas_serializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from ..db_services import selectors
from datetime import date
from ..models import Dresses, dress_busy_days


def check_if_request_user_is_dress_owner(request: HttpRequest, dress: Dresses) -> bool:
    """Check if the request user is the owner of the dress."""
    user = request.user
    return bool(selectors.get_investmenter_dresses_object(dress, user))


def dress_has_future_bookings(dress: Dresses) -> bool:
    today = date.today()
    # Query for future busy days related to the dress
    current_or_future_busy_days = dress_busy_days.objects.filter(
        dress=dress, busy_day__gte=today
    )
    # Check if there are any future bookings
    return current_or_future_busy_days.exists()


def delete_dress(request: HttpRequest):
    serializer = parmas_serializer.dress_params_serializer(data=request.GET)

    if not serializer.is_valid():
        return ({"status": "error", "data": serializer.errors}, HTTP_400_BAD_REQUEST)
    validted_data = serializer.data
    dress_uuid = validted_data.get("dress_uuid")

    dress = selectors.get_dress_by_id(dress_uuid)
    if not dress:
        return ({"status": "error", "data": "dress not found"}, HTTP_400_BAD_REQUEST)

    if not check_if_request_user_is_dress_owner(request, dress):
        return (
            {"status": "error", "data": "you are not the owner of this dress"},
            HTTP_400_BAD_REQUEST,
        )

    if dress_has_future_bookings(dress):
        dress.status = "unavailable"
        dress.save()
        return (
            {
                "status": "error",
                "data": "the dress have booking days in future so we will make it to unavailable for booking untill the booking days are over",
            },
            HTTP_200_OK,
        )
    dress.delete()
    return (
        {"status": "success", "data": "the dress deleted successfully"},
        HTTP_200_OK,
    )
