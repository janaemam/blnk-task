from django.db import models
from funds.models import BaseLoanFund  
# Create your models here.
class LoanPlan(models.Model):
    name = models.CharField(max_length=100)
    loan_fund = models.ForeignKey(BaseLoanFund, on_delete=models.CASCADE)
    interest_rate = models.FloatField()
    min_value = models.FloatField()
    max_value = models.FloatField()
    duration = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class LoanRequest(models.Model):
    loan_plan = models.ForeignKey(LoanPlan, on_delete=models.CASCADE)
    user = models.ForeignKey('users.Customer', on_delete=models.CASCADE)
    principal = models.FloatField()
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    request_status = models.CharField(max_length=50, choices=[('PENDING', 'Pending'), ('APPROVED','Approved'),('REJECTED','Rejected')])
    loan_officer = models.ForeignKey('users.BankPersonnel', on_delete=models.SET_NULL, null=True)  


    def __str__(self):
        return f"{self.user} - {self.loan_plan.name} - {self.request_status}"

class Loan(models.Model):
    loan_plan = models.ForeignKey(LoanPlan, on_delete=models.CASCADE)
    user = models.ForeignKey('users.Customer', on_delete=models.CASCADE)
    paid = models.FloatField()
    total = models.FloatField()  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user} - {self.loan_plan.name} - {self.total}"

class LoanPayment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount = models.FloatField()
    paid_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.Customer', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.loan} - {self.amount}"


    