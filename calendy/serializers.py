

from rest_framework import serializers
from .models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
       
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
     
        read_only_fields = ('created_at',)