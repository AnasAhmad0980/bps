from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from .models import User

def signup(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('budgeting_dashboard')
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        # Validation
        errors = []
        
        if not name:
            errors.append('Full name is required')
        
        if not email:
            errors.append('Email is required')
        elif '@' not in email:
            errors.append('Please enter a valid email address')
        
        if not password:
            errors.append('Password is required')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email already exists')
        
        if errors:
            return render(request, 'UserAuth/signup.html', {
                'errors': errors,
                'name': name,
                'email': email
            })
        
        try:
            # Create user
            user = User.objects.create_user(
                email=email,
                name=name,
                password=password
            )
            
            # Automatically log in the user
            auth_login(request, user)
            
            return redirect('budgeting_dashboard')
            
        except IntegrityError:
            errors.append('An error occurred. Please try again.')
            return render(request, 'UserAuth/signup.html', {
                'errors': errors,
                'name': name,
                'email': email
            })
    
    return render(request, 'UserAuth/signup.html')


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        return redirect('budgeting_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        
        errors = []
        
        if not email:
            errors.append('Email is required')
        
        if not password:
            errors.append('Password is required')
        
        if errors:
            return render(request, 'UserAuth/login.html', {
                'errors': errors,
                'email': email
            })
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Redirect to dashboard or the page they were trying to access
            next_url = request.GET.get('next', 'budgeting_dashboard')
            return redirect(next_url)
        else:
            errors.append('Invalid email or password')
            return render(request, 'UserAuth/login.html', {
                'errors': errors,
                'email': email
            })
    
    return render(request, 'UserAuth/login.html')


@login_required(login_url='login')
def logout_view(request):
    """Handle user logout"""
    auth_logout(request)
    return redirect('login')