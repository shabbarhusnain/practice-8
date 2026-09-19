from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
User=get_user_model()
class SignupForm(forms.Form):
    email=forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)
    def clean_email(self):
        email= self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already taken.')
        return email
    def clean_password1(self):
        password1=self.cleaned_data.get('password1')
        validate_password(password1)
        return password1
    def clean(self):
        cleaned_data= super().clean()
        p1= cleaned_data.get('password1')
        p2= cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2','Password do not match.')
        return cleaned_data 

class ResetForm(forms.Form):
    password1= forms.CharField(widget=forms.PasswordInput)
    password2= forms.CharField(widget=forms.PasswordInput)
    def password1_clean(self):
        password1=self.cleaned_data['password1']
        validate_password(password1)
        return password1
    def clean(self):
        cleaned_data= super().clean()
        p1= cleaned_data.get('password1')
        p2= cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password1', 'Password did not match :( ')
        return cleaned_data

# class RoleChoiceForm(forms.Form):
#     role_choice=[
#         ('Seeker','seeker'),
#         ('Educated_provider','educated_provider'),
#         ('Uneducated_provider','uneducated_provider')
#     ]
#     role=
