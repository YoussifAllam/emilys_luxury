from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CustomTokenObtainPairView,
    current_user,
    update_user,
    forgot_password,
    reset_password,
    APILogoutView,
    set_user_permissions,
    GoogleLoginRedirectView,
    GoogleLoginCallbackView,
    TokenValidationAPIView,
    get_username_by_uuid , 
    get_uuid_by_Email , 
    get_num_of_total_users ,
    Get_ALL_Users , 
    UserAPIView , 
    subscription_plan_count , 
    get_all_Merchants , 
    IncrementUserFieldView , 
)

from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet,basename='users')

urlpatterns = [
    path('', include(router.urls)),
    
    path('user/confirm-email/', UserViewSet.as_view({'post': 'confirm_email'}), name='confirm-email'),
    path('user/resend-otp/', UserViewSet.as_view({'post': 'send_reset_otp'}), name='send-reset-otp'),
    path('user/login/', CustomTokenObtainPairView.as_view(), name='user-login'),
    
    path("google-login/", GoogleLoginRedirectView.as_view(), name="google_login_redirect"),
    path("google-callback/", GoogleLoginCallbackView.as_view(), name="google_login_callback"),

    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('userinfo/', current_user,name='user_info'), 
    path('userinfo/update/', update_user,name='update_user'), 
    
    path('forgot_password/', forgot_password,name='forgot_password'), 
    path('reset_password/<str:token>',reset_password,name='reset_password'), 
    
    path('user/logout/', APILogoutView.as_view(), name='logout_token'),

    path('set-user-permissions/<str:username>/', set_user_permissions, name='set_user_permissions'),

    path('check_if_user_isAuthenticated/',TokenValidationAPIView.as_view() ) ,
    path('get_username_by_uuid/' , get_username_by_uuid) ,
    path('get_uuid_by_Email/' , get_uuid_by_Email) ,
    path('get_num_of_total_users/' , get_num_of_total_users.as_view()),
    path('Get_ALL_Users/' ,Get_ALL_Users ),
    path('get_users_info_by_uuids/' , UserAPIView.as_view()) , 
    path('subscription-plan-count/', subscription_plan_count, name='subscription_plan_count'),
    path('increment-field/', IncrementUserFieldView.as_view(), name='increment-field'),

    path('get_all_Merchants/' , get_all_Merchants)

]