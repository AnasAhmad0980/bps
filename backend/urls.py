from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def homepage(request):
    """Homepage - redirects based on authentication status"""
    if request.user.is_authenticated:
        return redirect('budgeting_dashboard')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='home'),
    path('', include('UserAuth.urls')),
    path('budget/', include('Budgeting.urls')),
]