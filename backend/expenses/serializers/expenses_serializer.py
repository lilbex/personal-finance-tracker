from rest_framework import serializers
from expenses.models import Expenses
from budget.serializers import GetBudgetAllocationSerializer


class CreateExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ["item", "amount", "note"]


class GetExpensesSerializer(serializers.ModelSerializer):
    allocation = GetBudgetAllocationSerializer()

    class Meta:
        model = Expenses
        fields = ["id",
                  "allocation",
                  "item",
                  "amount",
                  "note",
                  "created_at",
                  "updated_at",]
