from django.urls import path
from .client_views import (
    ClientListCreateView, 
    ClientDetailView, 
    NextOfKinListCreateView,
    NextOfKinDetailView
    )
from .loan_views import (
    LoanForAgentListCreateView, 
    LoanDecisionView, 
    # ClientLoanListView,
    ClientLoanApplicationCreateListView,
    ClientLoanApplicationDetailView
    )

urlpatterns = [
    # Agents
    path("agents/clients/", ClientListCreateView.as_view(), name="agent-clients"),
    path("agents/clients/<int:pk>", ClientDetailView.as_view(), name="client-detail"),
    path("agents/clients/<int:pk>/next-of-kin", NextOfKinListCreateView.as_view(), name="client-next-of-kin"),
    path("agents/clients/<int:pk>/next-of-kin/<int:id>", NextOfKinDetailView.as_view(), name="client-next-of-kin-detail"),
    path("agents/clients/<int:pk>/loan-application", ClientLoanApplicationCreateListView.as_view(), name="client-loan"),
    path("agents/clients/<int:pk>/loan-application/<int:id>", ClientLoanApplicationDetailView.as_view(), name="client-loan-detail"),
    # path("agents/loans/", LoanForAgentListCreateView.as_view(), name="agent-loans"),
    
    # Admin decision
    path(
        "admin/loans/<int:pk>/decision/",
        LoanDecisionView.as_view(),
        name="loan-decision",
    ),
   
    # Client view
    # path("clients/loans/", ClientLoanListView.as_view(), name="client-loans"),
]
