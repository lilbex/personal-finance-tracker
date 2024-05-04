from rest_framework import serializers
from budget.models import BudgetCategory


class CreateBudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = ["image", "name", "note",]

class GetBudgetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetCategory
        fields = '__all__'
       
