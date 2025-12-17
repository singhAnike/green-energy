from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from ..models import Service, Appointment, ContactMessage
from ..serializers.service_serializers import (
    ServiceSerializer,
    AppointmentSerializer,
    ContactMessageSerializer
)

class ServiceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing services."""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """Set custom permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

class AppointmentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing appointments."""
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return appointments for the authenticated user."""
        user = self.request.user
        if user.is_staff or user.is_technician:
            return Appointment.objects.all()
        return Appointment.objects.filter(customer=user)

    def perform_create(self, serializer):
        """Set the customer to the current user when creating an appointment."""
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update the status of an appointment."""
        appointment = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in dict(Appointment.STATUS_CHOICES):
            return Response(
                {"status": "Invalid status"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        appointment.status = new_status
        appointment.save()
        return Response({"status": "Status updated"})

class ContactMessageViewSet(viewsets.ModelViewSet):
    """ViewSet for contact messages."""
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'get', 'head', 'options']  # No update/delete for contact form

    def get_queryset(self):
        """Return all messages for staff, none for others."""
        if self.request.user.is_staff:
            return ContactMessage.objects.all().order_by('-created_at')
        return ContactMessage.objects.none()

    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            self.permission_classes = [permissions.AllowAny]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        """Create a new contact message."""
        serializer.save(ip_address=self.get_client_ip())

    def get_client_ip(self):
        """Get the client's IP address."""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
