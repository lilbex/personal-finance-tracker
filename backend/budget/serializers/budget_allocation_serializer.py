from rest_framework import serializers
from budget.models import BudgetAllocation
from .budget_category_serializer import GetBudgetCategorySerializer
from .budget_serializer import GetBudgetSerializer


class CreateBudgetAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetAllocation
        fields = ["budget", "category", "amount", "note"]


class GetBudgetAllocationSerializer(serializers.ModelSerializer):
    budget = GetBudgetSerializer()
    category = GetBudgetCategorySerializer()

    class Meta:
        model = BudgetAllocation
        fields = ["id",
                  "budget",
                  "category",
                  "amount",
                  "note",
                  "created_at",
                  "updated_at",]
