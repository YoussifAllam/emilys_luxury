from ..models import Dresses
from apps.investment.models import investmenter_dresses
from apps.Users.models import User as User_model


def get_dress_by_id(dress_id):
    try:
        return Dresses.objects.get(id=dress_id)
    except Dresses.DoesNotExist:
        return None


def get_investmenter_dresses_object(dress: Dresses, user: User_model):
    try:
        investmenter_dresses.objects.get(dress=dress, user=user)
        return True
    except investmenter_dresses.DoesNotExist:
        return None
