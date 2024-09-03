from django.contrib import admin
from .models import LoanPlan, LoanRequest, Loan, LoanPayment

@admin.register(LoanPlan)
class LoanPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'loan_fund', 'interest_rate', 'min_value', 'max_value', 'duration', 'created_at', 'updated_at')
    search_fields = ('name', 'loan_fund__name')
    list_filter = ('created_at', 'interest_rate')
    ordering = ('-created_at',)

@admin.register(LoanRequest)
class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_plan', 'principal', 'total', 'request_status', 'loan_officer', 'created_at', 'updated_at')
    search_fields = ('user__username', 'loan_plan__name', 'request_status')
    list_filter = ('request_status', 'created_at')
    ordering = ('-created_at',)

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan_plan', 'paid', 'total', 'created_at', 'updated_at')
    search_fields = ('user__username', 'loan_plan__name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)

@admin.register(LoanPayment)
class LoanPaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'loan', 'amount', 'paid_at')
    search_fields = ('user__username', 'loan__id')
    list_filter = ('paid_at',)
    ordering = ('-paid_at',)
