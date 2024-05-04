from django.db import models
import uuid


class BudgetAllocation(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    budget = models.ForeignKey(
        "Budget", on_delete=models.CASCADE, related_name="budget_allocation", null=True, blank=True)

    category = models.ForeignKey(
        "BudgetCategory", on_delete=models.CASCADE, related_name="budget_allocation", null=True, blank=True)

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    note = models.TextField(null=False, blank=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="budget_allocation", null=True, blank=True)


    class Meta:
        ordering = ['created_at']
