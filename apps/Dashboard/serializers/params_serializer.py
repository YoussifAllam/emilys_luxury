from rest_framework.serializers import Serializer , UUIDField

class DressParamsSerializer(Serializer):
    dress_id = UUIDField(required=True)