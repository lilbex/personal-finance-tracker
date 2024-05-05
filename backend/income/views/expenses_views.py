from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q
from income.models import Income
from income.serializers import CreateIncomeSerializer, GetIncomeSerializer
from datetime import datetime, timedelta


class CreateIncomeView(generics.GenericAPIView):
    """
  Create expenses
    """
    serializer_class = CreateIncomeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request,):
        user = request.user
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response({"message": "income successfully saved"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Please input valid data and try again"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListAllUserIncome(generics.ListAPIView):
    """
    List all user income
    search by note and filter by date range
    """
    serializer_class = GetIncomeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset.filter(user=user)

        search_query = self.request.query_params.get('search', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            start_datetime = datetime.combine(start_date, datetime.min.time())
            queryset = queryset.filter(created_at__gte=start_datetime)

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            end_datetime = datetime.combine(end_date, datetime.min.time())
            queryset = queryset.filter(created_at__date__lte=end_datetime)

        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(note__icontains=search_query)
            )

        return queryset
