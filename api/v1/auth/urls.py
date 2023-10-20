from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', SignUpView.as_view()), 
    path('verifyotp/', VerifyOTP.as_view()),
    path('add-profile/', AddProfile.as_view()),
    path('forget-password/', ForgetPassword.as_view()),
    path('forget-password/otp-verify/', VerifyOTP.as_view()),
    path('forget-password/change-password/', ChangePassword.as_view()),
    path('resendotp/', ResendOtp.as_view()),
    path('change-email/', ChangeEmail.as_view()),
    path('change-email/verify-otp/', ChangeEmailVerification.as_view()),
    path('change-password/', ChangePassword.as_view()),
    path('edit-profile/', EditProfile.as_view()),
]