from celery import shared_task
from django.core.management import call_command

@shared_task
def release_old_temporary_bookings():
    call_command('release_old_temporary_bookings')
