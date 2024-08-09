from ..models import investmenter_details

def check_if_use_have_investmenter_details(user):
    try :
        investmenter_details.objects.get(user=user)
        return True
    except investmenter_details.DoesNotExist:
        return False
