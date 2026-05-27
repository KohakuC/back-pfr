from rest_framework import serializers
from .models import Service


"""
Serializers for the services app.

A serializer converts Django model instances to JSON format (and vice versa),
and handles data validation before saving to the database.

This module contains:
- ServiceSerializer: serializer for the service catalogue (handles all CRUD operations)
"""


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at', 'utilisateur']
