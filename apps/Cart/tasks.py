from django.utils import timezone
from datetime import datetime , timedelta
from rest_framework.status import HTTP_400_BAD_REQUEST , HTTP_200_OK
from apps.Dresses.models import Dresses

def check_if_the_startdate_does_not_passed(booking_start_date:str) -> bool:
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

def is_booking_duration_correct(booking_start_date_str: str, booking_end_date_str: str, booking_for_n_days: str) -> bool:
    # Assuming the date format is 'YYYY-MM-DD'
    booking_start_date = datetime.strptime(booking_start_date_str, '%Y-%m-%d').date()
    booking_end_date = datetime.strptime(booking_end_date_str, '%Y-%m-%d').date()   
    
    actual_duration = (booking_end_date - booking_start_date).days 
    return actual_duration == int(booking_for_n_days)

def booking_days_is_available(dress: Dresses, booking_start_date_str: str, booking_end_date_str: str) -> bool:
    # Convert string dates to datetime objects
    booking_start_date = datetime.strptime(booking_start_date_str, '%Y-%m-%d').date()
    booking_end_date = datetime.strptime(booking_end_date_str, '%Y-%m-%d').date()

    busy_days = dress.busy_day_set.values_list('busy_day', flat=True)
    
    current_date = booking_start_date
    while current_date <= booking_end_date:
        if current_date in busy_days:
            return False
        current_date += timedelta(days=1)
    return True

def is_dress_available(dress :Dresses):
    if  dress.status  == 'unavailable': 
        return False
    return True

def process_is_valid(dress: Dresses, booking_for_n_days: str, booking_start_date: str, booking_end_date: str) -> bool:
    
    if booking_for_n_days not in ['3','6','8'] :
        return ({'status': 'fialed' , 'error': 'booking_for_n_days must be 3,6 or 8'}, HTTP_400_BAD_REQUEST)
    
    if not is_dress_available(dress) : 
        return ({'status': 'fialed' , 'error': 'The dress is not available for booking'}, HTTP_400_BAD_REQUEST)

    if not check_if_the_startdate_does_not_passed(booking_start_date) : 
        return ({'status': 'fialed' , 'error': 'The start date is passed'}, HTTP_400_BAD_REQUEST)
    
    if not is_booking_duration_correct(booking_start_date, booking_end_date, booking_for_n_days) : 
        return ({'status': 'fialed' , 'error': 'The duration is not correct'}, HTTP_400_BAD_REQUEST)
    
    if not booking_days_is_available(dress, booking_start_date, booking_end_date) :
        return ({'status': 'fialed' , 'error': 'The booking days are not available'}, HTTP_400_BAD_REQUEST)
    
    if  dress.status  == 'unavailable': 
        return ({'status': 'fialed' , 'error': 'The dress is not available for booking'}, HTTP_400_BAD_REQUEST)
    
    return ({'status': 'success'}, HTTP_200_OK)

