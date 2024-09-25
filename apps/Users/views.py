import random
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.decorators import action, permission_classes
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login as django_login
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes, parser_classes
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .permissions import IsAdminOrPostOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework.parsers import MultiPartParser, FormParser
from .services import GoogleRawLoginFlowService
from django.shortcuts import redirect
import requests
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()
from .models import *
from .serializers import *
from . import constant
from django.core.mail import EmailMessage
from .Tasks import get_device_info_tasks, invitaion_tasks


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [IsAdminOrPostOnly]
    lookup_field = "uuid"

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            invitaion_user_code = request.data.get("invitaion_code", None)
            if invitaion_user_code:
                invitaion_tasks.add_points_to_user(invitaion_user_code)

            user = serializer.save()

            # Generate a 4-digit OTP and store it in the user's profile
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            # Generate the HTML content for the OTP email
            html_message = constant.create_otp_template(
                f"{user.first_name} {user.last_name}", otp, user.email
            )

            # Send the OTP to the user via email
            subject = f"Your verification OTP on {constant.current_site}"
            email = EmailMessage(
                subject=subject,
                body=html_message,
                to=[user.email],
            )
            email.content_subtype = "html"  # Set the email content type to HTML
            email.send()

            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)
            token_data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            user_data = {
                "email_verified": serializer.data.get("email_verified"),
                "user_type": serializer.data.get("user_type"),
            }

            return Response(
                {"user": user_data, "tokens": token_data},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    # @permission_classes([IsAuthenticated])
    def confirm_email(self, request):
        # user_uuid = request.data.get('user_uuid')
        otp = request.data.get("otp")

        try:
            # user = User.objects.get(uuid=user_uuid)
            user = request.user
            if user.email_verified:
                return Response(
                    {"detail": "Email already confirmed."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if user.otp == int(otp) and self.is_otp_valid(user.otp_created_at):
                user.email_verified = True
                user.save()
                return Response(
                    {"detail": "Email confirmed successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "detail": "Unable to verify your email address with provided OTP."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"detail": "Invalid user ID."}, status=status.HTTP_400_BAD_REQUEST
            )

    def is_otp_valid(self, otp_created_at):
        # Check if the OTP is still valid based on the expiration time
        if otp_created_at:
            expiration_time = otp_created_at + timezone.timedelta(minutes=15)
            return timezone.now() <= expiration_time
        return False

    @action(detail=False, methods=["post"])
    def send_reset_otp(self, request):
        try:
            user = request.user
            if not user:
                return Response(
                    {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )

            # Generate a new 4-digit OTP and update it in the user's profile
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.save()

            # Generate the HTML content using create_otp_template
            html_message = constant.create_otp_template(
                f"{user.first_name} {user.last_name}", otp, user.email
            )

            # Send the OTP as an HTML email
            subject = f"Your reset OTP on {constant.current_site}"
            email = EmailMessage(
                subject=subject,
                body=html_message,
                to=[user.email],
            )
            email.content_subtype = "html"  # Set the email content type to HTML
            email.send()

            return Response(
                {"detail": "Reset OTP sent successfully."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Error sending OTP: {}".format(str(e))},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)

    user.username = data.get("username", user.username)

    if "password" in data and data["password"] != "":
        user.password = make_password(data["password"])

    # Check if 'profile_picture' is present in the request data
    if "profile_picture" in request.data:
        user.profile_picture = request.data["profile_picture"]

    if not user.created_Date:
        user.created_Date = timezone.now()

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


def get_current_host(request):
    if request.is_secure():
        protocol = "https"
    else:
        protocol = "http"
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)


@api_view(["POST"])
def forgot_password(request):
    data = request.data

    # Get the user object
    user = get_object_or_404(User, email=data["email"])

    # Generate a token and expiration time
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=10)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()

    # Get operating system and browser name
    operating_system, browser_name = get_device_info_tasks.get_device_info(request)

    # Create the reset link
    reset_link = f"{constant.rest_password_url}?token={token}"

    # Use the template creation function to generate the email body
    body = constant.create_password_reset_template(
        f"{user.first_name} {user.last_name}",
        reset_link,
        operating_system,
        browser_name,
    )

    # Send the email
    send_mail(
        "Password reset from Emily",
        body,
        f"{settings.EMAIL_HOST_USER}",
        [data["email"]],
        html_message=body,  # Ensure this is sent as an HTML email
    )

    return Response({"details": f'Password reset sent to {data["email"]}'})


@api_view(["POST"])
def reset_password(request, token):
    data = request.data
    try:
        user = User.objects.get(profile__reset_password_token=token)
    except User.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response(
            {"error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if data["password"] != data["confirmPassword"]:
        return Response(
            {"error": "Password are not same"}, status=status.HTTP_400_BAD_REQUEST
        )

    user.password = make_password(data["password"])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({"details": "Password reset done "})


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            if not user.is_active:
                return Response(
                    {"message": "Your account has been deactivated"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            if not user.email_verified:
                return Response(
                    {
                        "user": LoginUserSerializer(user).data,
                        "message": "Please activate email",
                        "tokens": data,
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            django_login(
                request, user, backend="django.contrib.auth.backends.ModelBackend"
            )

            return Response(
                {"user": LoginUserSerializer(user).data, "tokens": data},
                status=status.HTTP_200_OK,
            )
        # check if email not exist
        elif user is None:
            return Response(
                {"message": "Email not found"}, status=status.HTTP_401_UNAUTHORIZED
            )

        else:
            return Response(
                {"message": "Email or Password Error"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()


class GoogleLoginRedirectView(PublicApi):
    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleRawLoginFlowService()

        authorization_url, state = google_login_flow.get_authorization_url()

        request.session["google_oauth2_state"] = state

        # redirect to authorization_url
        return redirect(authorization_url)


class GoogleLoginCallbackView(PublicApi):

    def get(self, request, *args, **kwargs):
        service = GoogleRawLoginFlowService()
        code = request.GET.get("code")
        state = request.GET.get("state")
        session_state = request.session.get("google_oauth2_state")

        if code is None or state is None:
            return Response(
                {"error": "Code and state are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if state != session_state:
            return Response(
                {"error": "Invalid state parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
        credentials = service.get_access_token(code, redirect_uri)

        if "access_token" not in credentials:
            return Response(
                {"error": "Access token not found in response."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        access_token = credentials["access_token"]
        user_info = service.get_user_info(access_token)

        email = user_info.get("email")
        if not email:
            return Response(
                {"error": "Email not found in user info."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # if not found user crete new user
        users_with_email = User.objects.filter(email=email)

        if not users_with_email.exists():
            profile_picture_url = user_info.get("picture")
            if profile_picture_url:
                response = requests.get(profile_picture_url)
                if response.status_code == 200:
                    # upload image from gogle
                    profile_picture = SimpleUploadedFile(
                        name="profile_picture.jpg",
                        content=response.content,
                        content_type="image/jpeg",
                    )
                    user = User.objects.create(
                        email=user_info.get("email"),
                        username=user_info.get("email"),
                        first_name=user_info.get("given_name"),
                        # last_name=user_info.get("family_name"),
                        email_verified=True,
                        profile_picture=profile_picture,
                    )
                    access_token, refresh_token = service.get_access_and_refresh_tokens(
                        user
                    )
                    response_data = {
                        "message": "User created successfully.",
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token),
                    }

            else:
                user = User.objects.create(
                    email=user_info.get("email"),
                    username=user_info.get("email"),
                    first_name=user_info.get("given_name"),
                    # last_name=user_info.get("family_name"),
                    email_verified=True,
                )
                access_token, refresh_token = service.get_access_and_refresh_tokens(
                    user
                )
                response_data = {
                    "message": "User created successfully.",
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token),
                }

        user = users_with_email.first()
        access_token, refresh_token = service.get_access_and_refresh_tokens(user)
        response_data = {
            "access_token": str(access_token),
            "refresh_token": str(refresh_token),
        }

        user.last_login = datetime.now()
        user.save()

        return Response(response_data, status=status.HTTP_200_OK)


class APILogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get("refresh_token")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        logout(request)
        return Response({"status": "OK, goodbye"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def set_user_permissions(request, username):
    # Check if the requesting user is a superuser or staff
    if not (request.user.is_superuser or request.user.is_staff):
        return Response(
            {"error": "You do not have permission to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    is_staff = data.get("is_staff", False)
    is_superuser = data.get("is_superuser", False)

    # Only superusers can set superuser flag
    if request.user.is_superuser:
        user.is_superuser = is_superuser

    # Both superusers and staff can set staff flag
    user.is_staff = is_staff

    user.save()

    return Response(
        {"message": "User permissions updated successfully"}, status=status.HTTP_200_OK
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_type(request):
    Target_user_type = request.data.get("user_type", None)
    print(Target_user_type)
    if Target_user_type != "Investor" and Target_user_type != "Customer":
        return Response(
            {"error": "Invalid user type choises are only 'Investor' or 'Customer'"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = request.user
    user.user_type = Target_user_type
    user.save()
    return Response(
        {"message": "User type updated successfully"}, status=status.HTTP_200_OK
    )


@api_view(["Post"])
@permission_classes([IsAuthenticated])
def is_password_correct(request):
    user = request.user
    if user.check_password(request.data.get("password", " ")):
        return Response({"status": "success"}, status.HTTP_200_OK)
    else:
        return Response({"status": "faild"}, status.HTTP_400_BAD_REQUEST)
