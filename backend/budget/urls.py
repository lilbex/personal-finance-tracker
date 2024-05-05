from django.urls import path

from budget.views import (
    BudgetCategoryList,
    CreateBudgetView,
    GetBudgetListView,
    CreateBudgetAllocationView,
    ListBudgetAllocationsView,
    ListUserBudgetAllocationsView
)


urlpatterns = [
    path('list-category/', BudgetCategoryList.as_view(), name="list-category"),
    path('create-budget/', CreateBudgetView.as_view(), name='create-budget'),
    path('list-budget/', GetBudgetListView.as_view(),
         name='list-budgets'),
    path('create-budget-allocation/', CreateBudgetAllocationView.as_view(), name='create-budget-allocatio'),
    path('list-budget-allocation/<uuid:budget_id>/', ListBudgetAllocationsView.as_view(), name='list-budget-allocation'),
        path('list-user-budget-allocation/', ListUserBudgetAllocationsView.as_view(), name='list-user-budget-allocation'),

]
