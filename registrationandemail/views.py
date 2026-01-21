from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from student.models import *
from .tokens import email_verification_token

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if not all([username, email, first_name, last_name, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
        
        try:
            # Create user but set as inactive until email verification
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                is_active=False  # User inactive until verified
            )
            
            # Send verification email
            current_site = get_current_site(request)
            subject = 'Verify your email address'
            token = email_verification_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            
            verification_link = f"http://{current_site.domain}/verify-email/{uid}/{token}/"
            
            message = f"""
            Hi {user.first_name},
            
            Thank you for registering! Please click the link below to verify your email address:
            
            {verification_link}
            
            If you didn't create this account, please ignore this email.
            
            Best regards,
            Your Team
            """
            print('mail code hit')
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print('message sent')
            messages.success(request, "Registration successful! Please check your email to verify your account.")
            return redirect('login')
            
        except Exception as e:
            print(f"Error creating user: {e}")
            messages.error(request, "Something went wrong. Please try again.")
            return redirect('register')

    return render(request, 'register.html')


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_verification_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Email verified successfully! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Verification link is invalid or has expired.")
        return redirect('register')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('index')
            else:
                messages.error(request, "Please verify your email before logging in.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')
