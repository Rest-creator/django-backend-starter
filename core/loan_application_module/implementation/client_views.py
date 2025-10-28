from rest_framework import generics, permissions
from ..repository.client_repository import ClientRepository
from ..services.client_services import ClientService
from ..serializers.client_serializers import (
    ClientWriteSerializer,
    ClientReadSerializer,
    NextOfKinReadSerializer,
    NextOfKinWriteSerializer
)
from ..implementation.permissions import IsAgent, IsAgentOrAdmin
from .models import Client, NextOfKin

from django.shortcuts import get_object_or_404


class ClientListCreateView(generics.ListCreateAPIView):
    """
    Agents list their own clients & create new clients.
    """

    permission_classes = ( IsAgentOrAdmin, )

    def get_queryset(self):
        # return ORM queryset for DRF serializer - agents see their clients
        return (
            Client.objects.filter(created_by=self.request.user).order_by(
            "-created_at"
            ) if self.request.user.is_superuser == False
            else Client.objects.all().order_by("-created_at")
        )

    def get_serializer_class(self):
        return (
            ClientReadSerializer
                if self.request.method in permissions.SAFE_METHODS
            else ClientWriteSerializer
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( IsAgentOrAdmin, )
    
    def get_serializer_class(self):
        return (
            ClientReadSerializer 
                if self.request.method in permissions.SAFE_METHODS
            else  ClientWriteSerializer
        )
    
    def get_queryset(self):
         return (
            Client.objects.filter(created_by=self.request.user).order_by(
            "-created_at"
            ) if not self.request.user.is_superuser
            else Client.objects.all().order_by("-created_at")
        )
    

class NextOfKinListCreateView(generics.ListCreateAPIView):
    permission_classes = ( IsAgentOrAdmin, )

    def get_client_object(self):
        return get_object_or_404(Client, pk=self.kwargs.get("pk"))
    
    def get_queryset(self):
        return NextOfKin.objects.filter(client=self.get_client_object())
    
    def get_serializer_class(self):
        return (
            NextOfKinReadSerializer
              if self.request.method in permissions.SAFE_METHODS 
            else NextOfKinWriteSerializer
        )

    def perform_create(self, serializer):
        serializer.save(client=self.get_client_object())
    

class NextOfKinDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = ( IsAgentOrAdmin, )
    lookup_field = "id"

    def get_client_object(self):
        return get_object_or_404(Client, pk=self.kwargs.get("pk"))
    
    def get_queryset(self):
        return NextOfKin.objects.filter(client=self.get_client_object())
    
    def get_serializer_class(self):
        return (
            NextOfKinReadSerializer
              if self.request.method in permissions.SAFE_METHODS 
            else NextOfKinWriteSerializer
        )
