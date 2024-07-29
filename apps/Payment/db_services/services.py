
from ..models import Payment 

def create_payment_object(payment_id , data):
    
    payment = Payment.objects.create(
        id=payment_id,  # Use the returned ID from Moyasar
        amount=data['amount'],
        description=data['description'],
        status='pending'  # Explicitly set status
    )