from datetime import date
from apps.Dresses.models import Dresses, dress_busy_days

from datetime import datetime, timedelta


def dress_has_future_bookings(dress: Dresses) -> bool:
    today = date.today()
    # Query for future busy days related to the dress
    current_or_future_busy_days = dress_busy_days.objects.filter(
        dress=dress, busy_day__gte=today
    )
    # Check if there are any future bookings
    return current_or_future_busy_days.exists()


def dress_is_available(dress: Dresses) -> bool:
    return bool(dress.status == "available")


def booking_days_is_available(
    dress: Dresses, booking_start_date: str, booking_end_date: str
) -> bool:
    # Convert string dates to datetime objects
    # booking_start_date = datetime.strptime(booking_start_date_str, '%Y-%m-%d').date()
    # booking_end_date = datetime.strptime(booking_end_date_str, '%Y-%m-%d').date()

    busy_days = dress.busy_day_set.values_list("busy_day", flat=True)
    print("_________________________", busy_days)
    current_date = booking_start_date
    print("_________________________", current_date)

    while current_date <= booking_end_date:
        if current_date in busy_days:
            return False
        current_date += timedelta(days=1)
    return True
