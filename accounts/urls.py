from . import views 
from django.urls import path


app_name = 'accounts'

urlpatterns = [
  # URL pattern for user login
  path('home_login/', views.login_view, name='home_login'),
  path('logout/', views.logout_view, name='logout'),

  
  # URL pattern for user registration
  path('register/', views.register, name='register'),
  path('clear_messages/', views.clear_messages, name='clear_messages'),
  path('otp-verify/<str:username>/', views.otp_verify, name='otp_verify'),
  path('otp-login-verify/<str:username>/', views.otp_login_verify, name='otp_login_verify'),


]
