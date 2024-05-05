from django.urls import path

from expenses.views import (CreateExpensesView,
                            ListExpensesForCategoryAllocation,
                            ListAllBudgetExpenses)


urlpatterns = [
    path('create-expenses/<uuid:allocation_id>/',
         CreateExpensesView.as_view(), name="create-expenses"),
    path('list-budget-allocation-expenses/<uuid:allocation_id>/',
         ListExpensesForCategoryAllocation.as_view(), name='list-budget-allocation-expenses'),
    path('list-budget-expenses/<uuid:budget_id>/', ListAllBudgetExpenses.as_view(),
         name='list-budget-expenses'),

]
