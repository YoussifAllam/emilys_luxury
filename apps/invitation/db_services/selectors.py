from apps.invitation.models import user_invitation_points as user_invitation_points_model
# from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST
from apps.Users.models import User as USER_Model


def get_user_points(User: USER_Model) -> int :
    user_points , created = user_invitation_points_model.objects.get_or_create(user = User , num_of_points =0)
    return user_points