from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.db.models import Sum
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework import status, response
from rest_framework import permissions

from expenses.models import Expense
from income.models import Income
from expenses.permissions import IsOwner


class ExpenseSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_amount_for_category(self, expenses_list, category):
        category_expense = expenses_list.filter(category=category)
        amount = category_expense.aggregate(sum=Sum('amount'))['sum'] or 0.00
        return {'amount': amount}

    def get(self, request):
        now = datetime.now()
        a_year_ago = now - relativedelta(year=1)
        expenses = Expense.objects.filter(
            owner=request.user, date__gte=a_year_ago, date__lte=now)
        final = {}
        categories = expenses.values_list('category', flat=True).distinct()

        for category in categories:
            final[category] = self.get_amount_for_category(expenses, category)

        return response.Response(
            {'category_data': final}, status=status.HTTP_200_OK)


class IncomeSummaryStats(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_amount_for_sources(self, sources_list, source):
        source_income = sources_list.filter(source=source)
        amount = source_income.aggregate(sum=Sum('amount'))['sum'] or 0.00
        return {'amount': amount}

    def get(self, request):
        now = datetime.now()
        a_year_ago = now - relativedelta(year=1)
        income = Income.objects.filter(
            owner=request.user, date__gte=a_year_ago, date__lte=now)
        final = {}
        sources = income.values_list('source', flat=True).distinct()

        for source in sources:
            final[source] = self.get_amount_for_sources(income, source)

        return response.Response(
            {'source_data': final}, status=status.HTTP_200_OK)
