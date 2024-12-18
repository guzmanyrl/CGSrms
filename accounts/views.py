from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .forms import RegistrationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser 
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta
from django.template.loader import render_to_string
import random
from django.shortcuts import reverse
from django.contrib.auth import logout
from django.utils.cache import add_never_cache_headers
from django.http import HttpResponseRedirect

CustomUser = get_user_model()



@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Initially inactive until email verification
            user.is_email_verified = False
            user.save()

            # Generate OTP and save to user model
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()

            # Debugging: Print OTP and user details
            print(f"Generated OTP: {otp} for user: {user.username}")

            # Send OTP email
            send_mail(
                subject='Your OTP for Email Verification',
                message=f'Your one-time password (OTP) is {otp}. It is valid for 1 minute.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            # Redirect to OTP verification page
            return redirect('accounts:otp_verify', username=user.username)

    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

@csrf_protect
def otp_verify(request, username):
    user = get_object_or_404(CustomUser, username=username)
    otp_valid_duration = timedelta(minutes=1)
    time_elapsed = timezone.now() - user.otp_created_at
    remaining_time = int((otp_valid_duration - time_elapsed).total_seconds())

    # Debugging: Check time elapsed
    print(f"Time elapsed for OTP: {time_elapsed}, Remaining time: {remaining_time} seconds")

    # Redirect if time has expired
    if time_elapsed > otp_valid_duration:
        messages.error(request, 'OTP expired. Please request a new OTP.')
        return redirect('accounts:register')  # Allow them to go back to registration

    elif request.method == 'POST':
        otp = request.POST.get('otp')

        # Debugging: Print OTP values
        print(f"Entered OTP: {otp}, Expected OTP: {user.otp}")

        # Validate OTP
        if otp and otp == user.otp:
            user.is_email_verified = True
            user.is_active = True
            user.is_approved = False  # User is active but still needs admin approval
            
            # Optionally reset the OTP for security after successful verification
            user.otp = None
            user.otp_created_at = None
            
            user.save()

            messages.success(request, 'OTP verified successfully! You are now waiting for admin approval.')
            return redirect('accounts:home_login')  # Redirect to login after success
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
           

    return render(request, 'otp_verification.html', {
        'username': username,
        'remaining_time': remaining_time,
        'redirect_url': reverse('accounts:home_login')
    })
    
@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "GET":
        form = AuthenticationForm()  # Initialize an empty form
        return render(request, 'home_login.html', {'form': form})

    # For POST request: process login
    username = request.POST.get('username')
    password = request.POST.get('password')

    # Fetch the user using the provided username
    user = CustomUser.objects.filter(username=username).first()

    if user is None:
        messages.error(request, _("Invalid username or password."))
        return render(request, 'home_login.html', {'form': AuthenticationForm()})

    # Check if the user is approved
    if not user.is_approved:
        messages.error(request, _("Your account is locked. Please contact the admin."))
        return render(request, 'home_login.html', {'form': AuthenticationForm()})

    # Check for login attempt limit
    if user.login_attempts >= 3:
        messages.error(request, _("Your account is locked due to too many failed attempts. Ask the admin to unlock your account."))
        return render(request, 'home_login.html', {'form': AuthenticationForm()})

    # Authenticate the user with the provided password
    user_auth = authenticate(request, username=username, password=password)
    if user_auth is not None:
        # If authentication is successful, generate OTP for the user
        otp = str(random.randint(100000, 999999))  # Generate a new OTP
        user.otp = otp
        user.otp_created_at = timezone.now()  # Set the OTP creation time
        user.otp_attempts = 0  # Reset OTP attempts
        user.save()

        # Send the OTP via email
        send_mail(
            subject='Your OTP for Login Verification',
            message=f'Your one-time password (OTP) is {otp}. It is valid for 1 minute.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Redirect to OTP verification page
        return redirect('accounts:otp_login_verify', username=user.username)

    else:
        # Increment login attempts on failed authentication
        user.login_attempts += 1
        user.save()

        remaining_attempts = 3 - user.login_attempts
        if remaining_attempts > 0:
            messages.error(request, _(f"Invalid credentials. You have {remaining_attempts} attempts left out of 3."))
        else:
            messages.error(request, _("Your account is locked due to too many failed attempts. Contact Admin to unlock your account."))
            user.is_approved = False  # Lock the account after 3 failed attempts
            user.save()

    # Return the login form with error messages if authentication fails
    return render(request, 'home_login.html', {'form': AuthenticationForm()})



@csrf_protect
def otp_login_verify(request, username):
    user = get_object_or_404(CustomUser, username=username)
    otp_valid_duration = timedelta(minutes=1)
    time_elapsed = timezone.now() - user.otp_created_at

    if time_elapsed > otp_valid_duration:
        messages.error(request, 'OTP expired. Please try logging in again.')
        return redirect('accounts:home_login')  # Expired OTP, redirect to login

    if request.method == 'POST':
        otp = request.POST.get('otp')

        if otp and otp == user.otp:
            # OTP verified successfully, reset login attempts
            user.login_attempts = 0
            user.otp = None  # Clear OTP after successful verification
            user.otp_created_at = None
            user.otp_attempts = 0  # Reset OTP attempts
            user.save()

            # Log the user in and redirect to the dashboard or home page
            login(request, user)
            return redirect('CGS_Dashboard:dashboard')  # Redirect to the appropriate page

        else:
            # Increment OTP attempts on failed OTP verification
            user.otp_attempts += 1
            remaining_otp_attempts = 3 - user.otp_attempts
            user.save()

            if remaining_otp_attempts > 0:
                messages.error(request, _(f"Invalid OTP. You have {remaining_otp_attempts} attempts left."))
            else:
                # Lock account after 3 failed OTP attempts
                user.is_approved = False  # Lock account due to failed OTP attempts
                user.save()
                messages.error(request, _("Your account is locked due to too many failed OTP attempts. Contact Admin to unlock your account."))
                return redirect('accounts:home_login')

    return render(request, 'otp_verification_login.html', {'username': username})



@csrf_protect
@require_GET
def clear_messages(request):
    messages.get_messages(request).used = True 
    return HttpResponse('<ul class="messages hidden"></ul>')


@csrf_protect
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)  # Log the user out
    messages.success(request, "You have successfully logged out.")
    
    # Check if the request is an HTMX request
    if request.headers.get('HX-Request') == 'true':
        return JsonResponse({'redirect': reverse('accounts:home_login')})

    # For non-HTMX, use a standard HTTP redirect
    return HttpResponseRedirect(reverse('accounts:home_login'))

