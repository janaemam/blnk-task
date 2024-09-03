from django.db import models

class BaseLoanFund(models.Model):
    FUND_TYPES = [
        ('BIG', 'Big Loans Fund'),
        ('MEDIUM', 'Medium Loans Fund'),
        ('SMALL', 'Small Loans Fund'),
    ]
    
    type = models.CharField(max_length=10, choices=FUND_TYPES, unique=True)
    start_fund = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    current_value = models.FloatField()

    def __str__(self):
        return f"{self.get_type_display()} - Start Fund: {self.start_fund}, Current Value: {self.current_value}"
