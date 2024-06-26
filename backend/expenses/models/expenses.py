from django.db import models
import uuid


class Expenses(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    allocation = models.ForeignKey(
        "budget.BudgetAllocation", on_delete=models.CASCADE, related_name="expenses", null=True, blank=True)
    item = models.CharField(max_length=225)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    note = models.TextField()
    receipt = models.ImageField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="expenses", null=True, blank=True)

    class Meta:
        ordering = ['created_at']
