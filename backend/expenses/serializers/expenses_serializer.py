from rest_framework import serializers
from budget.models import BudgetAllocation
from expenses.models import Expenses
from budget.serializers import GetBudgetAllocationSerializer


class CreateExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ["item", "amount", "note"]


class GetBudgetSerializer(serializers.ModelSerializer):
    allocation = GetBudgetAllocationSerializer()

    class Meta:
        model = BudgetAllocation
        fields = ["id",
                  "allocation",
                  "item",
                  "amount",
                  "note",
                  "created_at",
                  "updated_at",]
