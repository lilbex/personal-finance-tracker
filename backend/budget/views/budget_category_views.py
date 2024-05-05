from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from budget.models import BudgetCategory
from budget.serializers import GetBudgetCategorySerializer

class BudgetCategoryList(APIView):
    """
    List all budget categories.
    """

    def get(self, request):
        categories = BudgetCategory.objects.all()
        serializer = GetBudgetCategorySerializer(categories, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
