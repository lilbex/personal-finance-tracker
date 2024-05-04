from django.db import models
import uuid
from authentication.models import User

class BudgetSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="budget_settings")

    allow_spend_beyond_budget = models.BooleanField(default=False, help_text="Allow users to spend beyond their budget.")

    budget_period_choices = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annually', 'Annually'),
    ]
    budget_period = models.CharField(max_length=20, choices=budget_period_choices, default='monthly', help_text="Select the period for budgeting.")

    currency_choices = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]
    currency = models.CharField(max_length=3, choices=currency_choices, default='USD', help_text="Select the currency for budget amounts.")

    budget_threshold_notification = models.BooleanField(default=True, help_text="Send notifications when users reach budget thresholds.")
    threshold_notification_percentage = models.PositiveIntegerField(default=80, help_text="Percentage of budget reached to trigger a notification.")

    budget_roll_over = models.BooleanField(default=False, help_text="Carry over unused budget amounts to the next period.")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Budget settings for {self.user}"
