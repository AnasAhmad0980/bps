# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required(login_url='login')
def dashboard(request):
    """Main dashboard with budget, calendar, goals, etc."""
    user = request.user
    
    # TODO: Get user's budgets, transactions, goals when models are ready
    # monthly_budget = MonthlyBudget.objects.filter(user=user).first()
    # goals = Goal.objects.filter(user=user)
    # recent_transactions = Transaction.objects.filter(user=user).order_by('-date')[:5]
    
    context = {
        'user': user,
        # 'monthly_budget': monthly_budget,
        # 'goals': goals,
        # 'recent_transactions': recent_transactions,
    }
    
    return render(request, 'Budgeting/dashboard.html', context)