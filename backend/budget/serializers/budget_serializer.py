from rest_framework import serializers
from budget.models import Budget


class CreateBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["start_date", "end_date", "amount", "note"]


class GetBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id",
                  "start_date",
                  "end_date",
                  "amount",
                  "note",
                  "created_at",
                  "updated_at",]
