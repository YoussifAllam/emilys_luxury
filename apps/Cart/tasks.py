from django.utils import timezone
from datetime import datetime

def check_if_the_startdate_does_not_passed(booking_start_date):
    try:
        # Assuming booking_start_date is a string in the format 'YYYY-MM-DD'
        booking_start_date = datetime.strptime(booking_start_date, '%Y-%m-%d')
        # Make booking_start_date timezone-aware
        booking_start_date = timezone.make_aware(booking_start_date, timezone.get_current_timezone())
    except ValueError:
        # Handle the error if the date format is incorrect
        return False
    
    if booking_start_date <= timezone.now():
        return False
    else:
        return True
