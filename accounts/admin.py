from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
from .forms import CustomUserForm
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib import messages
from unfold.admin import ModelAdmin  # Import ModelAdmin from unfold
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group, Permission
from django.contrib import admin

CustomUser = get_user_model()

# Action to approve selected users
@admin.action(description='Approve selected users')
def approve_users(modeladmin, request, queryset):
    for user in queryset:
        user.is_approved = True
        user.is_active = True  # Activate user when approved
        user.login_attempts = 0  # Reset login attempts
        user.save()

        # Send email notification to the approved user
        send_mail(
            subject='Account Approved',
            message=f'Hello {user.first_name} {user.last_name}, your account has been approved! You can now log in to the system.\n\n'
                    f'Login here: http://127.0.0.1:8000/',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

    messages.success(request, 'Selected users have been approved and activation emails sent.')

# Register the CustomUser model with the CustomUserAdmin
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin,ModelAdmin):  # Inherit from unfold's ModelAdmin
    form = UserChangeForm 
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = [
        'username', 'first_name', 'middle_name', 'last_name', 
        'email', 'is_active', 'is_approved', 'is_email_verified', 
        'login_attempts', 'date_joined', 'last_login'
    ]
    readonly_fields = ['last_login']  # Make last_login read-only
    list_filter = ['is_active', 'is_approved', 'is_email_verified']

    fieldsets = (
        (None, {
            'fields': (
                'username', 'first_name', 'middle_name', 'last_name', 
                'password', 'email', 'is_approved', 'is_email_verified'
            )
        }),  # Display is_email_verified
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}), 
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'first_name', 'middle_name', 'last_name', 
                'password1', 'password2', 'email', 'is_active', 
                'is_staff', 'is_superuser'
            )
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'middle_name', 'last_name')  # Allow searching by username or email
    ordering = ('username',)

    # Override the default queryset to show all users
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset  # Return all users

    actions = [approve_users]  # Register the approve_users action


# Unregister the default Group admin
admin.site.unregister(Group)

# Custom admin for Group model

# Optional: Customize Permission model admin (if needed)

    
    
    
# Set the custom admin branding

