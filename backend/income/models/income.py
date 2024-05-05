from django.db import models
import uuid


class Income(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    amount = models.DecimalField(max_digits=15, decimal_places=2)
    note = models.TextField(null=False, blank=False)
    date_received = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="income", null=True, blank=True)

    class Meta:
        ordering = ['created_at']
