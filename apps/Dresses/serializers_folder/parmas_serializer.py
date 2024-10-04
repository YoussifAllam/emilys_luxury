from rest_framework.serializers import Serializer, UUIDField


class dress_params_serializer(Serializer):
    dress_uuid = UUIDField(required=True)
