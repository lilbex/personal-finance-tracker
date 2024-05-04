from rest_framework import status, generics
from utils.response import Response
from budget.models import BudgetCategory
from rest_framework.views import APIView

# Use APIView here to remove pagination that is setup in settings.py


class CreateBudget(APIView):

    pass
