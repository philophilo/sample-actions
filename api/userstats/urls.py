from django.urls import path

from userstats.views import ExpenseSummaryStats, IncomeSummaryStats


urlpatterns = [
    path(
        "expenses-summary-stats",
        ExpenseSummaryStats.as_view(),
        name="expenses-summary-stats",
    ),
    path(
        "income-summary-stats",
        IncomeSummaryStats.as_view(),
        name="income-summary-stats"
    ),
]
