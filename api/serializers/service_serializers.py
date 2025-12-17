from rest_framework import serializers
from ..models import Service, Appointment, ContactMessage

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for the Service model."""
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class AppointmentSerializer(serializers.ModelSerializer):
    """Serializer for the Appointment model."""
    service_name = serializers.CharField(source='service.name', read_only=True)
    customer_name = serializers.SerializerMethodField()
    technician_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Appointment
        fields = [
            'id', 'customer', 'customer_name', 'service', 'service_name', 
            'technician', 'technician_name', 'scheduled_date', 'status', 
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at', 'customer')
    
    def get_customer_name(self, obj):
        return f"{obj.customer.get_full_name() or obj.customer.username}"
    
    def get_technician_name(self, obj):
        if obj.technician:
            return f"{obj.technician.get_full_name() or obj.technician.username}"
        return None
    
    def validate(self, data):
        """Validate the appointment data."""
        if 'scheduled_date' in data and data['scheduled_date'] < timezone.now():
            raise serializers.ValidationError({"scheduled_date": "Appointment date cannot be in the past."})
        return data

class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for the ContactMessage model."""
    class Meta:
        model = ContactMessage
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'is_read')
