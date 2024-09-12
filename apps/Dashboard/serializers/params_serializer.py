from rest_framework.serializers import Serializer , UUIDField ,FileField,ListField ,IntegerField

class DressParamsSerializer(Serializer):
    dress_id = UUIDField(required=True)

class DressImagesParamsSerializer(Serializer):
    dress_id = UUIDField(required=True)
    images = FileField(required=True)


class IDListSerializer(Serializer):
    ids = ListField(
        child=IntegerField(),  # Adjust the type according to your ID field (e.g., UUIDField for UUIDs)
        allow_empty=False
    )