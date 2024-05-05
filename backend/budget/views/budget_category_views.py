from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from budget.models import BudgetCategory
from budget.serializers import GetBudgetCategorySerializer, CreateBudgetCategorySerializer


class CreateBudgetCategory(generics.CreateAPIView):
    """
    Create budget category
    """

    queryset = BudgetCategory.objects.all()
    serializer_class = CreateBudgetCategorySerializer


class BudgetCategoryList(APIView):
    """
    List all budget categories.
    """

    def get(self, request):
        categories = BudgetCategory.objects.all()
        serializer = GetBudgetCategorySerializer(categories, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
