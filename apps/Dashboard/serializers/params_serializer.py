from rest_framework.serializers import Serializer , UUIDField ,FileField

class DressParamsSerializer(Serializer):
    dress_id = UUIDField(required=True)

class DressImagesParamsSerializer(Serializer):
    dress_id = UUIDField(required=True)
    images = FileField(required=True)