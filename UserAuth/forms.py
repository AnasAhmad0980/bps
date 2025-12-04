# FILE: UserAuth/forms.py
# ============================================================================

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class SignUpForm(UserCreationForm):
    """Form for user registration"""
    
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'full name',
            'class': 'form-input'
        })
    )
    
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'email',
            'class': 'form-input'
        })
    )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password',
            'class': 'form-input'
        })
    )
    
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'confirm password',
            'class': 'form-input'
        })
    )
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class LoginForm(AuthenticationForm):
    """Form for user login"""
    
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'username or email',
            'class': 'form-input'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'password',
            'class': 'form-input'
        })
    )

