from django.urls import path

from income.views import (CreateIncomeView,
                             ListAllUserIncome)


urlpatterns = [
    path('create-income/', CreateIncomeView.as_view(), name="create-income"),
    path('list-income/', ListAllUserIncome.as_view(), name='list-income')

]
