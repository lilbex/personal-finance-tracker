from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from budget.models import BudgetAllocation
from expenses.models import Expenses
from expenses.serializers import CreateExpensesSerializer,GetExpensesSerializer
from budget.models import BudgetSettings, Budget

class CreateBudgetAllocationView(generics.GenericAPIView):
    """
    Create expenses against a budget allocation. If you set allow_spend_beyond_budget to true, then
    you can not add expenses if you have spend beyond the total expenses for that category or if
    the amount you want to spend plus amount spend so far is greater than the allocated amount. You can spend beyond your
    budget if you set spend beyoud budget to true
    """
    serializer_class = CreateExpensesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, allocation_id):
        try:
            allocation = BudgetAllocation.objects.get(id=allocation_id)
            expenses = Expenses.objects.filter(allocation=allocation)

            total_spend = expenses.aggregate(total_spend=Sum('amount'))['total_spend'] or 0

            if total_spend > allocation.amount and not BudgetSettings.allow_spend_beyond_budget:
                message = f"You have exhausted your budget for {allocation.category.name} and you do not want to spend beyond your budget. You may want to update your setting or increase the budget for {allocation.category.name}"
                return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)

            requested_amount = request.data.get('amount', 0)
            if total_spend + requested_amount > allocation.amount and not BudgetSettings.allow_spend_beyond_budget:
                message = f"You do not have sufficient budget for {allocation.category.name} and you do not want to spend beyond your budget. You may want to update your setting or increase the budget for {allocation.category.name}"
                return Response({"message": message}, status=status.HTTP_406_NOT_ACCEPTABLE)

            if allocation.user != request.user:
                return Response({"message": "You are not authorized to create a budget allocation for this budget."}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Expenses successfully saved"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Please input valid data and try again"}, status=status.HTTP_400_BAD_REQUEST)
        except BudgetAllocation.DoesNotExist:
            return Response({"message": "Budget allocation does not exist"}, status=status.HTTP_404_NOT_FOUND)


class ListExpensesForCategoryAllocation(generics.ListAPIView):
    """
    List all allocations for a specific budget.
    """
    serializer_class = GetExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        budget_id = self.kwargs.get('budget_id')
        queryset = Expenses.objects.filter(budget_id=budget_id)
        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class ListAllBudgetExpenses(generics.ListAPIView):
    """
    List all allocations created by the authenticated user.
    """
    serializer_class = GetExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        budget_id = self.kwargs.get('budget_id')
        budget = Budget.object.get(id=budget_id)
        queryset = Expenses.objects.filter(budget=budget)

        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(allocation__category__name__icontains=search_query) |
                Q(item__icontains=search_query) |
                Q(note__icontains=search_query)
            )

        return queryset

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
