from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
import time, random
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import *
from django.contrib.auth.models import Group
from django.db import transaction
# Create your views here.
User=get_user_model()
# 
def signup_view(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data['email']
            password=form.cleaned_data['password1']
            try:
                with transaction.atomic():
                    user=User.objects.create_user(
                        email=email,
                        password=password
                    )
                    user.is_active=False
                    user.save()
                    _send_otp(request,user.email)
                uidb64=urlsafe_base64_encode(force_bytes(email))
                messages.success(
                        request, "OTP has been sent! Please check your email."
                    )
                return redirect(f'/verify_otp/{uidb64}')
            except Exception as e:
                print(e)
                messages.error(request, 'Registration failed because email could not be sent. Please check your network or email address.')
                return render(request, "signup.html", {"form": form})
    else: 
        form=SignupForm() 
    return render(request, 'signup.html',{'form':form})
def _send_otp(request, email):
    otp= random.randint(100000, 999999)
    request.session['email']=email
    request.session['otp']=str(otp)
    request.session['expiry']=time.time()+60
    subject= 'Rozgar Connector Otp'
    body=f'Your Otp is: {otp}. do not share with anyone.'
    email=EmailMessage(
        subject=subject,
        body=body,
        to=[email]
    )
    email.send(fail_silently=True)
def verify_otp(request, uidb64):
    raw_email=urlsafe_base64_decode(uidb64).decode('utf-8')
    email=raw_email.lower().strip()
    saved_email= request.session.get('email')
    saved_otp= request.session.get('otp')
    expiry= request.session.get('expiry')

    if request.method=="POST":
        otp=request.POST.get('otp')
        print(f"Saved Email: {saved_email} | URL Email: {email}")
        print(f"Saved OTP: {saved_otp} | Input OTP: {otp}")
        print(f"Expiry Time: {expiry} | Current Time: {time.time()}")
        if saved_email==email and saved_otp==str(otp) and expiry> time.time():
            print("--- CHK: HUREEY! All conditions matched perfectly! ---")
            try:
                user=User.objects.get(email=email)
                user.is_active=True
                user.save()
                request.session.pop('email')
                request.session.pop('otp')
                request.session.pop('expiry')
                print(f"User {user.email} is now active!")
                return redirect(f'/role_choice/{uidb64}/')
            except Exception as e:
                print(e)
        else:
            print("--- CHK: Condition failed (OTP/Email/Expiry wrong) ---")
            messages.info(request,'Oops wrong otp or expired :(')
            return redirect(f'/verify_otp/{uidb64}/')
    return render(request,'verify_otp.html',{'uidb64':uidb64,'expiry':expiry, 'time':time.time()})
def resend_otp(request, uidb64):
    raw_email= urlsafe_base64_decode(uidb64).decode('utf-8')
    email=raw_email.lower().strip() 
    _send_otp(request, email)
    return redirect(f'/verify_otp/{uidb64}/')
def forgot_password(request):
    if request.method=="POST":
        email=request.POST.get('email')
        if not User.objects.filter(email__iexact=email).exists():
            messages.info(request, 'This email does not exists :(')
            return redirect('/forgot_password/')
        else:
            _send_otp(request, [email])
            uidb64= urlsafe_base64_encode(force_bytes(email))
            return redirect(f'/verify_forgot_otp{uidb64}/')
    return render(request,'forgot_password.html')
def verify_forgot_otp(request, uidb64):
    raw_email= urlsafe_base64_decode(uidb64).decode('utf-8')
    email=raw_email.lower().strip()
    saved_email= request.session.get('email')
    saved_otp= request.session.get('otp')
    expiry= request.session.get('expiry')
    if request.method=="POST":
        otp=request.POST.get('otp')
        if saved_email==email and saved_otp==str(otp) and expiry>time.time():
            request.session.pop('email')
            request.session.pop('otp')
            request.session.pop('expiry')
            return redirect(f'/reset_password/{uidb64}/')
        else:
            messages.info(request,'Oops! Wrong otp or expired :(')
            return redirect(f'/verify_forgot_otp/{uidb64}/')
    return render(request,'verify_otp.html',{'uidb64':uidb64})    

def reset_password(request, uidb64):
    raw_email= urlsafe_base64_decode(uidb64).decode('utf-8')
    email=raw_email.lower().strip()
    form = ResetForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            password= form.cleaned_data['password1']
            user=User.objects.get(email=email)
            user.set_password(password)
            return redirect('/login/')
    return render(request, 'reset_password.html')
def login_view(request):
    if request.method=="POST":
        email= request.POST.get('email')
        password= request.POST.get('password')
        if not User.objects.filter(email=email).exists():
            messages.info(request,'User Not Found :(')
            return redirect('/login/')
        user=authenticate(request, username=email, password=password)
        if user==None:
            messages.info(request, 'Invalid Password!')
            return redirect('/login/')
        login(request, user)
        if user.role is None:
            uidb64=urlsafe_base64_encode(force_bytes(user.email))
            return redirect(f'/role_choice/{uidb64}/')
        if user.profile == False:
            print('user ki profile nahi bani to usay redirect kr diay ha')
            if user.role=='seeker':
                return redirect(f'/seeker_profile/')
            elif user.role=='educated_provider':
                return redirect(f'/educated_profile/')
            elif user.role=='uneducated_provider':
                return redirect(f'/uneducated_profile/')            
        return redirect('/home/')
    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect('/login/')
def role_choice(request, uidb64):
    if request.method=="POST":
        role= request.POST.get('role')
        raw_email= urlsafe_base64_decode(uidb64).decode('utf-8')
        email=raw_email.lower().strip()
        user= User.objects.get(email__iexact=email)
        user.role= role
        group, created= Group.objects.get_or_create(name=role)
        user.groups.add(group)
        user.save()
        if user.role=='seeker':
            return redirect(f'/seeker_profile/')
        elif user.role=='educated_provider':
            return redirect(f'/educated_profile/')
        elif user.role=='uneducated_provider':
            return redirect(f'/uneducated_profile/')
    return render(request, 'role_choice.html')
