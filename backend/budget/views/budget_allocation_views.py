from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from budget.models import BudgetAllocation
from budget.serializers import CreateBudgetAllocationSerializer, GetBudgetAllocationSerializer
from django.db.models import Q

class CreateBudgetAllocationView(APIView):
    """
    Create a new budget allocation.
    """
    serializer_class = CreateBudgetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # Ensure that the budget and category are associated with the authenticated user
            budget = serializer.validated_data['budget']
            category = serializer.validated_data['category']
            
            # Check if a budget allocation already exists for the same budget and category
            if BudgetAllocation.objects.filter(budget=budget, category=category).exists():
                return Response({"error": "You already allocated budget for this category."},
                                status=status.HTTP_409_CONFLICT)

            # Check if the budget is associated with the authenticated user
            if budget.logged_by != request.user:
                return Response({"error": "You are not authorized to create a budget allocation for this budget."},
                                status=status.HTTP_403_FORBIDDEN)

            serializer.save()
            return Response({"message":"Budget successfully allocated"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Please input valid data and try again"}, status=status.HTTP_400_BAD_REQUEST)



class ListBudgetAllocationsView(generics.ListAPIView):
    """
    List all allocations for a specific budget.
    """
    serializer_class = GetBudgetAllocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the budget_id from the URL query parameters
        budget_id = self.kwargs.get('budget_id')
        
        # Retrieve allocations for the specified budget
        queryset = BudgetAllocation.objects.filter(budget_id=budget_id)
        return queryset

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

        # Search functionality
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