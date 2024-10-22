from .. import models
from django.core.mail import EmailMessage
from django.conf import settings


def check_if_use_have_investmenter_details(user):
    try:
        models.investmenter_details.objects.get(user=user)
        return True
    except models.investmenter_details.DoesNotExist:
        return False


def send_email_for_admin(user, dress):
    for admin_email in [settings.ADMIN_EMAIL1, settings.ADMIN_EMAIL2]:
        email = EmailMessage(
            subject="New investment request",
            body=f""" User with email: {user.email}
                      has requested to invest in dress. with uuid: {dress.id},
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[admin_email],
        )
        email.send()
        print("email sent")
