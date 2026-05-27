from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

"""
Serializers for the administrator app.

A serializer converts Django model instances to JSON format (and vice versa),
and handles data validation before saving to the database.

This module contains:
- AdminUserListSerializer: serializes compact user's information for the admin list view
"""

class AdminUserListSerializer(serializers.ModelSerializer):
    """Compact representation of a user for the admin list view."""

    clients_count = serializers.IntegerField(read_only=True)
    quotes_count = serializers.IntegerField(read_only=True)
    invoices_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'username', 'first_name', 'last_name',
            'company_name', 'is_active', 'is_staff', 'date_joined',
            'last_login', 'clients_count', 'quotes_count', 'invoices_count',
        ]
        read_only_fields = fields
