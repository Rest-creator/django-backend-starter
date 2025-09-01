# loan/interfaces/views/client_views.py
from rest_framework import generics, permissions
from ..repository.client_repository import ClientRepository
from ..services.client_services import ClientService
from ..serializers.client_serializers import ClientCreateSerializer, ClientDetailSerializer
from ..implementation.permissions import IsAgent
from .models import Client

class ClientListCreateView(generics.ListCreateAPIView):
    """
    Agents list their own clients & create new clients.
    """
    permission_classes = [permissions.IsAuthenticated, IsAgent]
    serializer_class = ClientDetailSerializer  # default for GET

    def get_queryset(self):
        # return ORM queryset for DRF serializer - agents see their clients
        return Client.objects.filter(created_by=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        return ClientCreateSerializer if self.request.method == "POST" else ClientDetailSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
