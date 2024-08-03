from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.Dresses.models import dress_busy_days
from apps.orders.models import Order
from datetime import timedelta

class Command(BaseCommand):
    help = 'Release old temporary bookings'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timedelta(minutes=5)  # Adjust this duration as needed
        old_temporary_bookings = dress_busy_days.objects.filter(is_temporary=True, created_at__lt=expiration_time)
        count = old_temporary_bookings.count()
        old_temporary_bookings.delete()

        orders_expiration_time = timezone.now() - timedelta(minutes=60)
        not_paid_orders = Order.objects.filter(created_at__lt=orders_expiration_time , is_payment_completed =False)
        orders_count = not_paid_orders.count()
        not_paid_orders.delete()

        self.stdout.write(self.style.SUCCESS(f'Released {count} old temporary bookings and {orders_count} not paid orders'))
