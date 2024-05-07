from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from budget.models import BudgetAllocation, Budget, BudgetSettings, BudgetCategory
from budget.serializers import CreateBudgetAllocationSerializer, GetBudgetAllocationSerializer
from django.db.models import Q, Sum


class CreateBudgetAllocationView(generics.GenericAPIView):
    """
    Create a new budget allocation.
    """
    serializer_class = CreateBudgetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # Ensure that the budget and category are associated with the authenticated user
                budget_id = request.data['budget']
                budget = Budget.objects.get(id=budget_id)
                category = request.data['category']
                budget_category = BudgetCategory.objects.get(id=category)

                # Check if a budget allocation already exists for the same budget and category
                if BudgetAllocation.objects.filter(budget=budget, category=budget_category, user=user).exists():
                    return Response({"message": "You already allocated budget for this category."},
                                    status=status.HTTP_409_CONFLICT)

                # Ensure that the budget is associated with the authenticated user
                if budget.user != user:
                    return Response({"message": "You are not authorized to create a budget allocation for this budget."},
                                    status=status.HTTP_403_FORBIDDEN)

                # Check if total allocation exceeds budget amount and spending beyond budget is not allowed
                allocation = BudgetAllocation.objects.filter(budget=budget)
                total_allocation = sum(int(obj.amount) for obj in allocation)
                requested_amount = request.data.get('amount', 0)
                total = total_allocation + int(requested_amount)

                budget_settings = BudgetSettings.objects.get(user=user)

                if total > int(budget.amount) and budget_settings.allow_spend_beyond_budget == False:

                    return Response({"message": 'Enable allow spending beyond budget or increase your budget'}, status=status.HTTP_406_NOT_ACCEPTABLE)

                serializer.save(
                    budget=budget, category=budget_category, user=request.user)
                return Response({"message": "Budget successfully allocated"}, status=status.HTTP_201_CREATED)
            except Budget.DoesNotExist:
                return Response({"message": "Budget does not exist."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please input valid data and try again"}, status=status.HTTP_400_BAD_REQUEST)


class ListBudgetAllocationsView(generics.ListAPIView):
    """
    List all allocations for a specific budget.
    """
    serializer_class = GetBudgetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        budget_id = self.kwargs.get('budget_id')
        return BudgetAllocation.objects.filter(budget_id=budget_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListUserBudgetAllocationsView(generics.ListAPIView):
    """
    List all allocations created by the authenticated user.
    """
    serializer_class = GetBudgetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = BudgetAllocation.objects.filter(logged_by=user)

        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(note__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
