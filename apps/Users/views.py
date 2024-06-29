import random
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import  login as django_login
from django.contrib.auth import logout
from rest_framework.decorators import api_view, permission_classes,parser_classes
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta
from .permissions import IsAdminOrPostOnly 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.parsers import MultiPartParser, FormParser
from .services import GoogleRawLoginFlowService
from django.shortcuts import redirect
import requests
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model() 

from django.core.exceptions import ValidationError

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from datetime import datetime as dt
from django.db.models import Q
from .models import *
from .serializers import *

class TokenValidationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        # print('Token: ', token , '______________________________________________________')
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Validate the token and get the payload
            untyped_token = UntypedToken(token)
            payload = untyped_token.payload
            
            # Extract the user ID from the token payload
            user_id = payload.get('user_id')
            if not user_id:
                return Response({'error': 'Invalid token payload'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Query the user model using the extracted user ID
            user = User.objects.get(id=user_id)
            serializer = get_user_curr_usage_serializer(user)

            Target_System_Limits, created = System_Limits.objects.get_or_create(
                Subscription_Type=user.subscription_plan ,
                defaults={
                    'Subscription_Type' : user.subscription_plan , 
                    'pin_limit' : 0 ,
                    'search_limit' : 0 ,
                    'team_members_limit' : 0, 
                }
            )
            System_Limits_serializer = get_System_limits_serializer(Target_System_Limits)
            
            return Response({
                'is_valid': True, 
                'user_curr_usage': serializer.data , 
                'System Limits': System_Limits_serializer.data
            }, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except (InvalidToken, TokenError) as e:
            return Response({'is_valid': False, 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [IsAdminOrPostOnly]
    lookup_field = 'uuid'


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            
            
            user = serializer.save()

            # Generate a 4-digit OTP and store it in the user's profile
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.otp_created_at = timezone.now()

            user.save()

            # Send the OTP to the user via email
            current_site = 'Baggr.com'
            subject = 'Your verification OTP on {0}'.format(current_site)
            message = f'Your verification OTP is: {otp}'
            user.email_user(subject, message)

            refresh = RefreshToken.for_user(user)
            token_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({'user': serializer.data, 'tokens': token_data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def confirm_email(self, request):   
        user_id = request.data.get('user_uuid')
        otp = request.data.get('otp')
        
        try:
            user = User.objects.get(uuid=user_id)
            if user.email_verified:
                return Response({'detail': 'Email already confirmed.'}, status=status.HTTP_400_BAD_REQUEST)

            print(self.is_otp_valid(user.otp_created_at) , "=================")
            print(user.otp == int(otp))            
            if user.otp == int(otp) and self.is_otp_valid(user.otp_created_at):
                user.email_verified = True
                user.save()
                return Response({'detail': 'Email confirmed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Unable to verify your email address with provided OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({'detail': 'Invalid user ID.'}, status=status.HTTP_400_BAD_REQUEST)
    
    def is_otp_valid(self, otp_created_at):
        # Check if the OTP is still valid based on the expiration time
        if otp_created_at:
            expiration_time = otp_created_at + timezone.timedelta(minutes=15)
            return timezone.now() <= expiration_time
        return False
    
    @action(detail=False, methods=['post'])
    def send_reset_otp(self, request):
        email = request.data.get('email', '')
        print(email)
        try:
            user = User.objects.get(email=email)

            # Generate a new 4-digit OTP and update it in the user's profile
            otp = random.randint(1000, 9999)
            user.otp = otp
            user.save()

            # Send the new OTP to the user via email
            current_site = 'Baggr.com'
            subject = 'Your reset OTP on {0}'.format(current_site)
            message = f'Your reset OTP is: {otp}'
            user.email_user(subject, message)

            return Response({'detail': 'Reset OTP sent successfully.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def update_user(request):
    user = request.user
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    # user.last_name = data.get('last_name', user.last_name)
    
    user.username = data.get('username', user.username)

    if 'password' in data and data['password'] != "":
        user.password = make_password(data['password'])

    # Check if 'profile_picture' is present in the request data
    if 'profile_picture' in request.data:
        user.profile_picture = request.data['profile_picture']

    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

def get_current_host(request):
    protocol = request.is_secure() and 'https' or 'http'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user = get_object_or_404(User,email=data['email'])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=10)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()
    
    host = get_current_host(request)
    # link = "http://localhost:8000/api/reset_password/{token}".format(token=token)
    link = "{host}reset_password/{token}".format(host=host,token=token)    
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "Paswword reset from Baggr",
        body,
        "Baggr@gmail.com",
        [data['email']]
    )
    return Response({'details': 'Password reset sent to {email}'.format(email=data['email'])})

@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    try:
        user = User.objects.get(profile__reset_password_token=token)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST
        )
    if user.profile.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response({'error': 'Token is expired'},status=status.HTTP_400_BAD_REQUEST)
    
    if data['password'] != data['confirmPassword']:
        return Response({'error': 'Password are not same'},status=status.HTTP_400_BAD_REQUEST)
    
    user.password = make_password(data['password'])
    user.profile.reset_password_token = ""
    user.profile.reset_password_expire = None 
    user.profile.save() 
    user.save()
    return Response({'details': 'Password reset done '})

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            if not user.is_active:
                return Response({'message': 'Your account has been deactivated'}, status=status.HTTP_403_FORBIDDEN)

            if not user.email_verified:
                return Response({'user_id': user.uuid,'message': 'Please activate email'}, status=status.HTTP_403_FORBIDDEN)
            
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            django_login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return Response({'user': UserSerializer(user).data, 'tokens': data}, status=status.HTTP_200_OK)
        #check if email not exist
        elif user is None:
            return Response({'message': 'Email not found'}, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
            return Response({'message': 'Email or Password Error'}, status=status.HTTP_401_UNAUTHORIZED)

class PublicApi(APIView):
    authentication_classes = ()
    permission_classes = ()
    
class GoogleLoginRedirectView(PublicApi):
    def get(self, request, *args, **kwargs):
        google_login_flow = GoogleRawLoginFlowService()

        authorization_url, state = google_login_flow.get_authorization_url()

        request.session["google_oauth2_state"] = state

        #redirect to authorization_url
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
                status=status.HTTP_400_BAD_REQUEST
            )
        if state != session_state:
            return Response(
                {"error": "Invalid state parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        
        redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
        credentials = service.get_access_token(code, redirect_uri)
        
        if "access_token" not in credentials:
            return Response(
                {"error": "Access token not found in response."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        access_token = credentials["access_token"]
        user_info = service.get_user_info(access_token)

        email = user_info.get("email")
        if not email:
            return Response(
                {"error": "Email not found in user info."},
                status=status.HTTP_400_BAD_REQUEST
            )
        #if not found user crete new user
        users_with_email = User.objects.filter(email=email)
        
        if not users_with_email.exists():
            profile_picture_url = user_info.get("picture")
            if profile_picture_url:
                response = requests.get(profile_picture_url)
                if response.status_code == 200:
                    #upload image from gogle 
                    profile_picture = SimpleUploadedFile(
                        name="profile_picture.jpg",
                        content=response.content,
                        content_type="image/jpeg"
                    )
                    user = User.objects.create(
                        email=user_info.get("email"),
                        username=user_info.get("email"),
                        first_name=user_info.get("given_name"),
                        # last_name=user_info.get("family_name"),
                        email_verified=True,
                        profile_picture=profile_picture
                    )
                    access_token, refresh_token = service.get_access_and_refresh_tokens(user)
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
                    email_verified=True
                )
                access_token, refresh_token = service.get_access_and_refresh_tokens(user)
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
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        logout(request)
        return Response({"status": "OK, goodbye"})
              
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_user_permissions(request, username):
    # Check if the requesting user is a superuser or staff
    if not (request.user.is_superuser or request.user.is_staff):
        return Response({"error": "You do not have permission to perform this action"}, status=status.HTTP_403_FORBIDDEN)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    is_staff = data.get('is_staff', False)
    is_superuser = data.get('is_superuser', False)

    # Only superusers can set superuser flag
    if request.user.is_superuser:
        user.is_superuser = is_superuser

    # Both superusers and staff can set staff flag
    user.is_staff = is_staff

    user.save()

    return Response({"message": "User permissions updated successfully"}, status=status.HTTP_200_OK)


class get_num_of_total_users(APIView):
    """
    View to list all services and their number of categories.
    """
    def get(self, request):
        
        total_users = User.objects.all().distinct().count()
        Pending_Approvals = User.objects.filter(is_approvid=False).count()
        return Response({
            
            "Num of Total Users": total_users ,
            "Pending_Approvals": Pending_Approvals

            })
    
# class Get_ALL_Users(APIView):
@api_view(['GET'])
def Get_ALL_Users(request):
    users = User.objects.all()
    serializer = GetALLUserSerializer(users, many=True)
    return Response({   
            'status': 'success',
            'data' : serializer.data
            } , status= status.HTTP_200_OK
        )


@api_view(['GET'])
def get_username_by_uuid(request):
    user_uuid = request.GET.get('user_uuid', None)
    if not user_uuid:
        return Response({"error": "user_uuid parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = Get_UserNameSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
def get_uuid_by_Email(request):
    email = request.GET.get('email', None)
    if not email:
        return Response({"error": "email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = Get_UserNameSerializer(user)
    return Response(serializer.data)


class UserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        uuids = request.data.get('uuids', [])
        if not uuids:
            return Response({'error': 'No UUIDs provided'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(uuid__in=uuids)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def subscription_plan_count(request):
    # Query the database to count the occurrences of each subscription plan
    subscription_counts = User.objects.values('subscription_plan').annotate(count=Count('subscription_plan'))
    
    # Convert the queryset to a dictionary for easy JSON serialization
    subscription_counts_dict = {item['subscription_plan']: item['count'] for item in subscription_counts}
    
    # Return the counts as a JSON response using DRF's Response class
    return Response(subscription_counts_dict)

@api_view(['GET'])
def get_all_Merchants(request):
    merchants = User.objects.filter(User_Type = "Merchant")
    serializer = UserSerializer(merchants, many=True)
    return Response({
        'status': 'success',
        'data' :
        serializer.data}
        , status=status.HTTP_200_OK
        )

class IncrementUserFieldView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user_uuid = request.data.get('user_uuid')
        field_name = request.data.get('field_name')
        increment = request.data.get('increment', False)
        # print('================' , increment)

        allowed_fields = ['Pin_limit_rechecd', 'Search_limit_rechecd', 'Team_members_limit', 'subscription_plan']
        
        if field_name not in allowed_fields:
            return Response({'error': 'Invalid field name'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(uuid=user_uuid)
            current_value = getattr(user, field_name)
            
            if isinstance(current_value, int):
                if increment == True:
                    setattr(user, field_name, current_value + 1)
                else:
                    if current_value > 0:
                        setattr(user, field_name, current_value - 1)    
                user.save()
                return Response({
                    'message': f'{field_name} has been {"incremented" if increment else "decremented"}',
                    'new_value': getattr(user, field_name)
                }, status=status.HTTP_200_OK)
            else:
                raise ValidationError('The field is not an integer type.')
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

