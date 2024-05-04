from django.db import models
import uuid


class Budget(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.CharField(max_length=100, null=True, blank=True)
    note = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        "authentication.User", on_delete=models.CASCADE, related_name="budget", null=True, blank=True)

    class Meta:
        ordering = ['created_at']
