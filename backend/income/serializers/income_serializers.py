from rest_framework import serializers
from income.models import Income


class CreateIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['amount',
                  'note',
                  'date_received',]


class GetIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ["id",
                  "amount",
                  "note",
                  "date_received",
                  "created_at",
                  "updated_at",]
