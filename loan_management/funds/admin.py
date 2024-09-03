from django.contrib import admin
from .models import BaseLoanFund

class BaseLoanFundAdmin(admin.ModelAdmin):
    list_display = ('type', 'start_fund', 'current_value', 'created_at')
    list_filter = ('type',)
    search_fields = ('type', 'start_fund', 'current_value')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        """Customize the queryset for different user types if needed."""
        queryset = super().get_queryset(request)
        # You can filter the queryset based on user permissions here if needed
        return queryset

admin.site.register(BaseLoanFund, BaseLoanFundAdmin)
