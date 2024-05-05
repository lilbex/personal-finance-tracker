from rest_framework import status, generics
from rest_framework.response import Response
from budget.models import Budget
# from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from budget.serializers import CreateBudgetSerializer, GetBudgetSerializer


class CreateBudgetView(generics.GenericAPIView): # using this  view help properly generate documentation
    """
    Create a new budget.
    """
    serializer_class = CreateBudgetSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        # Set logged_by to the authenticated user's ID
        data["logged_by"] = request.user.id
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Please enter valid information and try again"}, status=status.HTTP_400_BAD_REQUEST)


class GetBudgetListView(generics.ListAPIView):
    """
    Retrieve all budgets associated with the authenticated user.
    """
    serializer_class = GetBudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Budget.objects.filter(logged_by=user).order_by('-created_at')

        # Search functionality
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(start_date__icontains=search_query) |
                Q(end_date__icontains=search_query) |
                Q(amount__icontains=search_query) |
                Q(note__icontains=search_query)
            )

        return queryset