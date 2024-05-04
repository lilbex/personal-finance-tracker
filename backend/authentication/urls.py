from django.urls import path

from authentication.views import (
    Login,
    RegisterView,
    ForgotPasswordRequestView,
    VerifyEmail,
    ResetPassword,
)


urlpatterns = [
    path('login/', Login.as_view(), name="register"),
    path('register/',RegisterView.as_view(), name='register'),
    path('forgot-password/',ForgotPasswordRequestView.as_view(), name='forgot-password'),
    path('verify-account/', VerifyEmail.as_view(), name='verify-account'),
    path('reset-password/', VerifyEmail.as_view(), name='reset-password'),

]
