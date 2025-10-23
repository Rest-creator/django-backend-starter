# loan/interfaces/views/loan_views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from ..repository.client_repository import ClientRepository
from ..repository.loan_repository import LoanRepository
from ..services.loan_services import LoanService
from ..serializers.loan_serializer import (
    LoanCreateSerializer,
    LoanDetailSerializer,
    LoanDecisionSerializer,
    LoanApplicationReadSerializer,
    LoanApplicationWriteSerializer
)
from .models import (
    LoanApplication,
    Client
    )
from .permissions import (
    IsAgent, 
    IsAdminReviewer, 
    IsAgentOrAdmin
    )


class LoanForAgentListCreateView(generics.ListCreateAPIView):
    """
    Agents list their submitted loans & create loan applications.
    """

    permission_classes = [permissions.IsAuthenticated, IsAgent]
    serializer_class = LoanDetailSerializer

    def get_queryset(self):
        return (
            LoanApplication.objects.filter(submitted_by=self.request.user)
            .select_related("client")
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        return (
            LoanCreateSerializer
            if self.request.method == "POST"
            else LoanDetailSerializer
        )

    def create(self, request, *args, **kwargs):
        service = LoanService(ClientRepository(), LoanRepository())
        data = request.data
        try:
            entity = service.submit_application(
                agent_id=request.user.id,
                client_id=int(data.get("client")),
                amount_requested=float(data.get("amount_requested")),
                term_months=int(data.get("term_months")),
                notes=data.get("notes", ""),
            )
            # Return ORM serializer for convenience (could map from entity too)
            obj = LoanApplication.objects.get(id=entity.id)
            return Response(
                LoanDetailSerializer(obj).data, status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoanDecisionView(generics.UpdateAPIView):
    """
    Admin reviews a single loan: approve or reject.
    """

    permission_classes = [permissions.IsAuthenticated, IsAdminReviewer]
    serializer_class = LoanDecisionSerializer
    queryset = LoanApplication.objects.all()

    def update(self, request, *args, **kwargs):
        loan_id = kwargs.get("pk")
        approve = bool(request.data.get("approve"))
        service = LoanService(ClientRepository(), LoanRepository())
        entity = service.decide(
            loan_id=loan_id, admin_id=request.user.id, approve=approve
        )
        if not entity:
            return Response(
                {"detail": "Loan not found"}, status=status.HTTP_404_NOT_FOUND
            )
        obj = LoanApplication.objects.get(id=entity.id)
        # TODO: send notification to client here
        return Response(LoanDetailSerializer(obj).data, status=status.HTTP_200_OK)


# class ClientLoanListView(generics.ListAPIView):
#     """
#     Clients (end users) view their loan applications.
#     Assumes request.user is linked to a Client via some relation OR
#     you pass ?client_id= in query params. Adjust to your auth model.
#     """

#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = LoanDetailSerializer

#     def get_queryset(self):
#         # Option A: use query param
#         client_id = self.request.query_params.get("client_id")
#         qs = LoanApplication.objects.none()
#         if client_id:
#             qs = LoanApplication.objects.filter(client_id=client_id).select_related(
#                 "client"
#             )
#         # Option B: resolve client via request.user.profile.client_id (if you store that)
#         return qs.order_by("-created_at")

class ClientLoanApplicationCreateListView(generics.ListCreateAPIView):
    permission_classes = ( IsAgentOrAdmin, )

    def get_client_object(self):
        return get_object_or_404(Client, pk=self.kwargs.get("pk"))
    
    def get_queryset(self):
        return LoanApplication.objects.filter(client=self.get_client_object())
    
    def get_serializer_class(self):
        return (
            LoanApplicationReadSerializer
                if self.request.method in permissions.SAFE_METHODS
            else LoanApplicationWriteSerializer
            )
    
    def perform_create(self, serializer):
        serializer.save(
            client=self.get_client_object(),
            submitted_by=self.request.user,
        )


class ClientLoanApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( IsAgentOrAdmin, )
    lookup_field = "id"

    def get_client_object(self):
        return get_object_or_404(Client, pk=self.kwargs.get("pk"))
    
    def get_queryset(self):
        return LoanApplication.objects.filter(client=self.get_client_object())
    
    def get_serializer_class(self):
        return (
            LoanApplicationReadSerializer
                if self.request.method in permissions.SAFE_METHODS
            else LoanApplicationWriteSerializer
            )
    
    def perform_update(self, serializer):
        serializer.save(
            reviewed_by=self.request.user
        )