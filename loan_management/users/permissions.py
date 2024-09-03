from rest_framework.permissions import BasePermission

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_customer)

class IsFundProvider(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_fund_provider)

class IsBankPersonnel(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_bank_personnel)
