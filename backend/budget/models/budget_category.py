from django.db import models
import uuid


class BudgetCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    image = models.ImageField(
        upload_to='budget_category/', null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
