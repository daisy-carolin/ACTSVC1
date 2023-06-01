from django.urls import path
from authentication.views import SignupView, RetrieveUserView, VerifyOTP, ActivateUserEmail
from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('sign_up/', SignupView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('verify_otp/', VerifyOTP.as_view(),name='verify_otp'),
    path('me/', RetrieveUserView.as_view(),name='retrieve_user'),
    path('api/users/activate/<int:user_id>/<str:confirmation_token>', ActivateUserEmail.as_view(), name='user_email_activation'),
    # path('otp/<str:uid>/', otpVerify, name='otp')
]


