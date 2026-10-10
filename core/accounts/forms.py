from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
User=get_user_model()
class SignupForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    father_name=forms.CharField()
    cnic=forms.IntegerField(max_value=13, min_value=13)
    address=forms.Textarea()
    district=forms.CharField()
    phone_number=forms.IntegerField()
    bio=forms.Textarea()
    profile_image=forms.ImageField(widget=forms.FileInput)
    cnic_front=forms.ImageField(widget=forms.FileInput)
    cnic_back=forms.ImageField(widget=forms.FileInput)
    email=forms.EmailField()
    password1=forms.CharField(widget=forms.PasswordInput)
    password2=forms.CharField(widget=forms.PasswordInput)
    def clean_cnic(self):
        cnic=self.cleaned_data['cnic']
        if User.objects.filter(cnic=cnic).exists():
            raise forms.ValidationError("This CNIC is already registered.")
        if len(cnic)<13 or len(cnic)>13:
            raise forms.ValidationError("Cnic must contains 13 digits only")
        return cnic
    def clean_profile_image(self):
        profile_image=self.cleaned_data['profile_image']
        mb=1024*1024
        if profile_image.size>mb:
            raise forms.ValidationError('Image size must be 1Mb or less then 1Mb')
        return profile_image
    def clean_cnic_front(self):
        cnic_front=self.cleaned_data['cnic_front']
        mb=1024*1024
        if cnic_front.size>mb:
            raise forms.ValidationError('Image size must be 1Mb or less then 1Mb')
        return cnic_front
    def clean_cnic_back(self):
        cnic_back=self.cleaned_data['cnic_back']
        mb=1024*1024
        if cnic_back.size>mb:
            raise forms.ValidationError('Image size must be 1Mb or less then 1Mb')
        return cnic_back
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
