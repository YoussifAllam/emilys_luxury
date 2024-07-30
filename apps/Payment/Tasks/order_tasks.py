from apps.orders import models as order_models
from apps.Payment import models as payment_models
from apps.Shipping import models as shipping_models
from apps.investment import models as investmenter_models


def do_related_tasks_for_order(order_uuid):
    """
    do_related_tasks_for_order
    this function will will pass for each dress in order and calc the investmenter new curr_balance 
    and create objects for dress booking days 
    """
    order = order_models.Order.objects.get(uuid=order_uuid)
    for dress in order.dresses.all():
        investmenter = dress.investmenter
        if not investmenter:
            continue