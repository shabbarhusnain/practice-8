from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User=get_user_model()
        email=username or kwargs.get('email')
        if email is None:
            print( ' if none de ra ha')
            return None
        try:
            user= User.objects.get(email__iexact=email)
            print("shabbar")
        except User.DoesNotExist:
            print('user nhi ka error')
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            print ("ye to chal raha ha")
            return user
        print('masla shuru sa ha')
        
    