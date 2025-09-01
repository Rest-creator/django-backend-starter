from django.urls import path
from .client_views import ClientListCreateView
from .loan_views import LoanForAgentListCreateView, LoanDecisionView, ClientLoanListView

urlpatterns = [
    # Agents
    path("agents/clients/", ClientListCreateView.as_view(), name="agent-clients"),
    path("agents/loans/", LoanForAgentListCreateView.as_view(), name="agent-loans"),

    # Admin decision
    path("admin/loans/<int:pk>/decision/", LoanDecisionView.as_view(), name="loan-decision"),

    # Client view
    path("clients/loans/", ClientLoanListView.as_view(), name="client-loans"),
]
