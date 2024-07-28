from django.utils import timezone
from datetime import datetime , date

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

def is_booking_duration_correct(booking_start_date_str: str, booking_end_date_str: str, booking_for_n_days: int) -> bool:
    # Assuming the date format is 'YYYY-MM-DD'
    booking_start_date = datetime.strptime(booking_start_date_str, '%Y-%m-%d').date()
    booking_end_date = datetime.strptime(booking_end_date_str, '%Y-%m-%d').date()   
    
    actual_duration = (booking_end_date - booking_start_date).days 
    return actual_duration == int(booking_for_n_days)