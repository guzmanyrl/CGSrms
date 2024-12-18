from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser



from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Replace with User if not using a custom model
        fields = ('username', 'first_name','middle_name','last_name', 'email', 'password1', 'password2')
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name','middle_name', 'last_name','password', 'is_active', 'is_staff', 'is_superuser', 'date_joined']  # Removed 'last_login'






class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username',)

