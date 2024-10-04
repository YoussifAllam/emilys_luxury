from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
)
from django.http import HttpRequest
from ..serializers import params_serializer, Investor_OutputSerializers
from ..db_services import selectors, services
from apps.Dresses.models import dress_images


def patch_investor_dresses(request: HttpRequest) -> tuple[dict, int]:
    serializer = params_serializer.DressParamsSerializer(data=request.GET)
    if not serializer.is_valid():
        return ({"status": "error", "data": serializer.errors}, HTTP_400_BAD_REQUEST)

    dress_id = serializer.validated_data.get("dress_id")
    dress_instance = selectors.get_dress_using_uuid(dress_id)
    if not dress_instance:
        return ({"status": "error", "data": "dress not found"}, HTTP_404_NOT_FOUND)

    Response_data, Response_status = services.patch_investor_dresses(
        request, dress_instance
    )
    return (Response_data, Response_status)


def dress_photo_upload(request: HttpRequest) -> tuple[dict, int]:
    serializer = params_serializer.DressImagesParamsSerializer(data=request.data)
    if not serializer.is_valid():
        return ({"status": "error", "data": serializer.errors}, HTTP_400_BAD_REQUEST)

    dress_id = serializer.validated_data.get("dress_id")
    dress_instance = selectors.get_dress_using_uuid(dress_id)
    if not dress_instance:
        return ({"status": "error", "data": "dress not found"}, HTTP_404_NOT_FOUND)

    # Process each photo in the request
    photos = request.FILES.getlist("images")
    services.create_dress_images_objects(dress_instance, photos)

    # You might want to return the URLs of the uploaded photos or just a success message
    return (
        {"status": "success", "message": "Photos uploaded successfully"},
        HTTP_201_CREATED,
    )


def get_dress_images(request: HttpRequest) -> tuple[dict, int]:
    serializer = params_serializer.DressParamsSerializer(data=request.GET)
    if not serializer.is_valid():
        return ({"status": "error", "data": serializer.errors}, HTTP_400_BAD_REQUEST)

    dress_id = serializer.validated_data.get("dress_id")
    dress_instance = selectors.get_dress_using_uuid(dress_id)
    if not dress_instance:
        return ({"status": "error", "data": "dress not found"}, HTTP_404_NOT_FOUND)

    # Initialize the serializer with the instance
    serializer = Investor_OutputSerializers.DressesSerializer(instance=dress_instance)

    return (serializer.data, HTTP_200_OK)


def delete_dress_images(request: HttpRequest) -> tuple[dict, int]:
    serializer = params_serializer.IDListSerializer(data=request.data)
    if not serializer.is_valid():
        return ({"status": "error", "data": serializer.errors}, HTTP_400_BAD_REQUEST)

    ids = serializer.validated_data.get("ids")

    # Delete the dress_images instances with the given IDs
    deleted_count, _ = dress_images.objects.filter(id__in=ids).delete()

    return (
        {"status": "success", "data": {"deleted_count": deleted_count}},
        HTTP_200_OK,
    )
