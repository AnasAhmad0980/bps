from django.contrib import admin
from .models import MonthlyBudget, Category, Transaction, DailySummary, MonthlySummary, Goal

@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'start_date', 'end_date', 'total_budget', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_date', 'created_at')
    search_fields = ('user__email', 'user__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_date'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'monthly_budget', 'allocated_amount', 'is_custom', 'created_at')
    list_filter = ('is_custom', 'category_type', 'created_at')
    search_fields = ('category_name', 'monthly_budget__user__email')
    readonly_fields = ('created_at',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'amount', 'category', 'date', 'monthly_budget', 'created_at')
    list_filter = ('transaction_type', 'date', 'created_at')
    search_fields = ('note', 'category__category_name', 'monthly_budget__user__email')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'

@admin.register(DailySummary)
class DailySummaryAdmin(admin.ModelAdmin):
    list_display = ('date', 'monthly_budget', 'total_income', 'total_expense', 'net_amount')
    list_filter = ('date',)
    search_fields = ('monthly_budget__user__email',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date'

@admin.register(MonthlySummary)
class MonthlySummaryAdmin(admin.ModelAdmin):
    list_display = ('monthly_budget', 'total_income', 'total_expense', 'remaining_balance', 'savings_rate')
    search_fields = ('monthly_budget__user__email',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'current_progress', 'target_date', 'is_completed')
    list_filter = ('is_completed', 'target_date', 'created_at')
    search_fields = ('title', 'user__email', 'user__name')
    readonly_fields = ('created_at', 'updated_at')