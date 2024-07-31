from apps.invitation.models import user_invitation_points  , invitation_points_Trade
# from rest_framework.status import HTTP_200_OK , HTTP_400_BAD_REQUEST
from apps.Users.models import User as USER_Model


def get_user_points(User: USER_Model) -> user_invitation_points :
    user_points, created = user_invitation_points.objects.get_or_create(user=User)
    if created:
        user_points.user_code = user_points.generate_unique_user_code()
        user_points.save()
    return user_points

def get_system_points_to_trade_obj() -> invitation_points_Trade:
    return invitation_points_Trade.objects.first()
