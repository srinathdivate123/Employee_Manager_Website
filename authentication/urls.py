from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from . import views
urlpatterns = [
    path('login', views.LoginView, name='nlogin'),
    path('logout', views.LogoutView, name='nlogout'),
    path('request-reset-link', views.RequestPasswordResetEmail, name='nreset'),
    path('set-new-password/<uidb64>/<token>', views.SetNewPasswordView, name='set-new-password'),
]