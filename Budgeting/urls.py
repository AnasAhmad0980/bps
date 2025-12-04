from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='budgeting_dashboard'),
    # More URLs will be added here as we build features:
    # path('budget/setup/', views.budget_setup, name='budget_setup'),
    # path('transactions/', views.transactions, name='transactions'),
    # path('goals/', views.goals, name='goals'),
]