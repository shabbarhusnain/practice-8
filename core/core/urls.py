"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import *
from user_profile.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # account app urls
    path('signup/', signup_view, name='signup'),
    path('verify_otp/<uidb64>/', verify_otp, name='verify_otp'),
    path('resend_otp/<uidb64>', resend_otp, name= 'resend_otp'),
    path('forgot_password/<uidb64>/', forgot_password, name='forgot_password'),
    path('verify_forgot_otp/<uidb64>/',verify_forgot_otp, name='verify_forgot_otp'),
    path('reset_password/<uidb64>/', reset_password, name='reset_password'),
    path('role_choice/<uidb64>/', role_choice, name='role_choice'),
    path('login/', login_view, name='login'),    
    path('logout/', logout_view, name= 'logout'),
    # user_profil app urls
    # path('seeker_profile/', seeker_profile, name='seeker_profile'),
    # path('educated_profile/',educated_profile, name= 'educated_profile'),
    # path('uneducated_profile/', uneducated_profile, name='uneducated_profile'),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)