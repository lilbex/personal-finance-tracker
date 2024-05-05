from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from budget.models import BudgetAllocation, Budget, BudgetSettings
from budget.serializers import CreateBudgetAllocationSerializer, GetBudgetAllocationSerializer
from django.db.models import Q, Sum


class CreateBudgetAllocationView(generics.GenericAPIView):
    """
    Create a new budget allocation.
    """
    serializer_class = CreateBudgetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                # Ensure that the budget and category are associated with the authenticated user
                budget_id = serializer.validated_data['budget']
                budget = Budget.objects.get(id=budget_id)
                category = serializer.validated_data['category']

                # Check if a budget allocation already exists for the same budget and category
                if BudgetAllocation.objects.filter(budget=budget, category=category).exists():
                    return Response({"error": "You already allocated budget for this category."},
                                    status=status.HTTP_409_CONFLICT)

                # Ensure that the budget is associated with the authenticated user
                if budget.logged_by != request.user:
                    return Response({"error": "You are not authorized to create a budget allocation for this budget."},
                                    status=status.HTTP_403_FORBIDDEN)

                # Check if total allocation exceeds budget amount and spending beyond budget is not allowed
                total_allocation = BudgetAllocation.objects.filter(
                    budget=budget).aggregate(total_spend=Sum('amount'))['total_spend'] or 0
                requested_amount = request.data.get('amount', 0)
                if total_allocation + requested_amount > budget.amount and not BudgetSettings.allow_spend_beyond_budget:

                    return Response({"message": 'Enable allow spending beyond budget or increase your budget'}, status=status.HTTP_406_NOT_ACCEPTABLE)

                serializer.save()
                return Response({"message": "Budget successfully allocated"}, status=status.HTTP_201_CREATED)
            except Budget.DoesNotExist:
                return Response({"error": "Budget does not exist."}, status=status.HTTP_404_NOT_FOUND)
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
