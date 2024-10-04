from apps.invitation.models import (
    user_invitation_points as user_invitation_points_model,
)


def add_points_to_user(invitaion_user_code):
    try:
        user_object = user_invitation_points_model.objects.get(
            user_code=invitaion_user_code
        )
        user_object.num_of_points += 1
        user_object.save()
    except user_invitation_points_model.DoesNotExist:
        pass
