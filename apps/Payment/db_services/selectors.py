from apps.investment import models as investmenter_models
from apps.Dresses.models import Dresses as Dresses_models
from apps.Users.models import User as User_model
from apps.orders.models import Order as order_model
def get_investor_detail_object( dress : Dresses_models ) -> investmenter_models.investmenter_details:
    try:
        investmenter_dress = investmenter_models.investmenter_dresses.objects.get(dress=dress)
        investmenter_detail = investmenter_models.investmenter_details.objects.get(user=investmenter_dress.user)
        
        return investmenter_detail
    except investmenter_models.investmenter_dresses.DoesNotExist:
        return None
    except investmenter_models.investmenter_details.DoesNotExist:
        return None
    
def get_investor_Balance_object(Target_user : User_model ) -> investmenter_models.investmenter_balance:
        investor_Balance_object , created = investmenter_models.investmenter_balance.objects.get_or_create(user=Target_user)
        return investor_Balance_object


def get_order_by_uuid(order_uuid ) ->  order_model:
    try:
        order = order_model.objects.get(uuid = order_uuid)
        return order
    except order_model.DoesNotExist:
        return None