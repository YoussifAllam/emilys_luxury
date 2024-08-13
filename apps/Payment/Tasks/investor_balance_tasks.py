from apps.orders import models as order_models
# from apps.Payment import models as payment_models
# from apps.Shipping import models as shipping_models
# from apps.investment import models as investmenter_models
# from apps.Users.models import User as User_model
from apps.SiteOwner_receivable import models as SiteOwner_receivable_models
from rest_framework.status import HTTP_200_OK 
from ..db_services import selectors
# from uuid import uuid4

def update_investor_balance(order : order_models.Order  ):
    """
    do_related_tasks_for_order
    this function will will pass for each dress in order and calc the investmenter new curr_balance 
    and create objects for dress booking days 
    """
    for order_item in order.items_set.all():
        response_data , response_status = add_investor_balance(order_item )
        # if response_status != HTTP_200_OK:
        # print (response_data, '\n', response_status)

    # return (response_data, HTTP_400_BAD_REQUEST) # todo --------------------------


def add_investor_balance(order_item :order_models.OrderItem  ): # , request_user: User_model
    SiteOwner_receivable_precentage = SiteOwner_receivable_models.SiteOwner_receivable.objects.first().Percentage
    investor_receivable_precentage = (100 - SiteOwner_receivable_precentage) / 100
    investor_receivable = order_item.price * (investor_receivable_precentage)

    investor_details_object = selectors.get_investor_detail_object(order_item.Target_dress)
    investor_Balance_object = selectors.get_investor_Balance_object(investor_details_object.user)
    
    total_balance , curr_balance = investor_Balance_object.total_balance , investor_Balance_object.curr_balance

    investor_Balance_object.total_balance = total_balance + investor_receivable
    investor_Balance_object.curr_balance  = curr_balance + investor_receivable
    investor_Balance_object.save()

    return ({'status': 'success' ,
              'curr_balance' : investor_Balance_object.curr_balance ,
              'total_balance' : investor_Balance_object.total_balance}, HTTP_200_OK)


# this function will use it in order refund
def reduce_investor_balance(order_item :order_models.OrderItem):
    SiteOwner_receivable_precentage = SiteOwner_receivable_models.SiteOwner_receivable.objects.first().Percentage
    investor_receivable_precentage = (100 - SiteOwner_receivable_precentage) / 100
    investor_receivable = order_item.price * (investor_receivable_precentage)

    investor_details_object = selectors.get_investor_detail_object(order_item.Target_dress)
    investor_Balance_object = selectors.get_investor_Balance_object(investor_details_object.user)
    
    total_balance , curr_balance = investor_Balance_object.total_balance , investor_Balance_object.curr_balance

    investor_Balance_object.total_balance = total_balance - investor_receivable
    investor_Balance_object.curr_balance  = curr_balance - investor_receivable
    investor_Balance_object.save()

    return ({'status': 'success' ,
              'curr_balance' : investor_Balance_object.curr_balance ,
              'total_balance' : investor_Balance_object.total_balance}, HTTP_200_OK)
    

