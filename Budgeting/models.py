from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class MonthlyBudget(models.Model):
    """Monthly budget with start and end dates"""
    budgetId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='budgets')
    start_date = models.DateField()
    end_date = models.DateField()
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'monthly_budgets'
        ordering = ['-start_date']
        unique_together = ['user', 'start_date']
    
    def __str__(self):
        return f"{self.user.name} - {self.start_date} to {self.end_date} - {self.total_budget}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate end_date as 30 days from start_date
        if not self.end_date and self.start_date:
            self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)
    
    def get_total_spent(self):
        """Calculate total expenses for this budget period"""
        transactions = self.transactions.filter(transaction_type='expense')
        return sum(t.amount for t in transactions)
    
    def get_total_income(self):
        """Calculate total income for this budget period"""
        transactions = self.transactions.filter(transaction_type='income')
        return sum(t.amount for t in transactions)
    
    def get_remaining_balance(self):
        """Calculate remaining balance"""
        return self.total_budget - self.get_total_spent()
    
    def get_categories_summary(self):
        """Get spending summary by category"""
        categories = self.categories.all()
        summary = []
        for category in categories:
            spent = category.get_spent()
            summary.append({
                'category': category,
                'allocated': category.allocated_amount,
                'spent': spent,
                'remaining': category.allocated_amount - spent,
                'percentage': (spent / category.allocated_amount * 100) if category.allocated_amount > 0 else 0
            })
        return summary


class Category(models.Model):
    """Budget categories (predefined + custom)"""
    PREDEFINED_CATEGORIES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('shopping', 'Shopping'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health & Fitness'),
        ('education', 'Education'),
        ('savings', 'Savings'),
        ('other', 'Other'),
    ]
    
    categoryId = models.AutoField(primary_key=True)
    monthly_budget = models.ForeignKey(MonthlyBudget, on_delete=models.CASCADE, related_name='categories')
    category_name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=50, choices=PREDEFINED_CATEGORIES, blank=True, null=True)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_custom = models.BooleanField(default=False)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        ordering = ['category_name']
    
    def __str__(self):
        return f"{self.category_name} - {self.allocated_amount}"
    
    def get_spent(self):
        """Calculate total spent in this category"""
        transactions = self.transactions.filter(transaction_type='expense')
        return sum(t.amount for t in transactions)
    
    def get_remaining(self):
        """Calculate remaining amount in this category"""
        return self.allocated_amount - self.get_spent()


class Transaction(models.Model):
    """Income and Expense transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    transactionId = models.AutoField(primary_key=True)
    monthly_budget = models.ForeignKey(MonthlyBudget, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.date}"


class DailySummary(models.Model):
    """Summary of transactions for each day"""
    summaryId = models.AutoField(primary_key=True)
    monthly_budget = models.ForeignKey(MonthlyBudget, on_delete=models.CASCADE, related_name='daily_summaries')
    date = models.DateField()
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # income - expense
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'daily_summaries'
        ordering = ['-date']
        unique_together = ['monthly_budget', 'date']
    
    def __str__(self):
        return f"{self.date} - Income: {self.total_income}, Expense: {self.total_expense}"
    
    @staticmethod
    def update_or_create_for_date(monthly_budget, date):
        """Update or create daily summary for a specific date"""
        transactions = Transaction.objects.filter(
            monthly_budget=monthly_budget,
            date=date
        )
        
        total_income = sum(
            t.amount for t in transactions.filter(transaction_type='income')
        )
        total_expense = sum(
            t.amount for t in transactions.filter(transaction_type='expense')
        )
        net_amount = total_income - total_expense
        
        summary, created = DailySummary.objects.update_or_create(
            monthly_budget=monthly_budget,
            date=date,
            defaults={
                'total_income': total_income,
                'total_expense': total_expense,
                'net_amount': net_amount,
            }
        )
        return summary


class MonthlySummary(models.Model):
    """Summary of entire budget period"""
    summaryId = models.AutoField(primary_key=True)
    monthly_budget = models.OneToOneField(MonthlyBudget, on_delete=models.CASCADE, related_name='summary')
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    savings_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Percentage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'monthly_summaries'
    
    def __str__(self):
        return f"Summary for {self.monthly_budget}"
    
    @staticmethod
    def update_or_create_for_budget(monthly_budget):
        """Update or create monthly summary for a budget"""
        total_income = monthly_budget.get_total_income()
        total_expense = monthly_budget.get_total_spent()
        remaining_balance = monthly_budget.get_remaining_balance()
        
        # Calculate savings rate
        if monthly_budget.total_budget > 0:
            savings_rate = ((monthly_budget.total_budget - total_expense) / monthly_budget.total_budget) * 100
        else:
            savings_rate = 0
        
        summary, created = MonthlySummary.objects.update_or_create(
            monthly_budget=monthly_budget,
            defaults={
                'total_income': total_income,
                'total_expense': total_expense,
                'remaining_balance': remaining_balance,
                'savings_rate': savings_rate,
            }
        )
        return summary


class Goal(models.Model):
    """Long-term savings goals"""
    goalId = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_progress = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'goals'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.current_progress}/{self.target_amount}"
    
    def get_progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount > 0:
            return (self.current_progress / self.target_amount) * 100
        return 0
    
    def get_remaining_amount(self):
        """Calculate remaining amount to reach goal"""
        return self.target_amount - self.current_progress
    
    def get_days_remaining(self):
        """Calculate days remaining to reach target date"""
        today = timezone.now().date()
        if self.target_date > today:
            return (self.target_date - today).days
        return 0