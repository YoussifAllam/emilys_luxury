
from ..models import Payment 
def create_payment_object(payment_id , data , Target_order_price):
    
    payment = Payment.objects.create(
        id=payment_id,  # Use the returned ID from Moyasar
        amount=Target_order_price,
        description=' TEST description', #TODO------------------
        status='pending'  # Explicitly set status
    )


