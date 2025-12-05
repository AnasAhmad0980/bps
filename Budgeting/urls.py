from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='budgeting_dashboard'),
    
    # Budget Setup
    path('budget/setup/', views.budget_setup, name='budget_setup'),
    path('budget/<int:budget_id>/categories/', views.category_setup, name='category_setup'),
    path('category/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    
    # Transactions
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/<int:transaction_id>/edit/', views.edit_transaction, name='edit_transaction'),
    path('transactions/<int:transaction_id>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/quick-add/', views.quick_add_transaction, name='quick_add_transaction'),
]