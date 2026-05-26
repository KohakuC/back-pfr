from rest_framework import serializers
from django.apps import apps

"""
Serializers for the clients app.

A serializer converts Django model instances to JSON format (and vice versa),
and handles data validation before saving to the database.

This module contains:
- AddressNestedSerializer: address serializer embedded inside ClientSerializer
- AddressSerializer: standalone serializer for the /addresses/ endpoints
- ClientSerializer: main serializer for the Client model, handles nested 
  address creation and update
"""

class AddressNestedSerializer(serializers.ModelSerializer):
    """Serializer for addresses nested inside ClientSerializer"""
    class Meta:
        model = apps.get_model('clients', 'Address')
        fields = ['id', 'type', 'ligne1', 'ligne2', 'code_postal', 'ville', 'pays', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('clients', 'Address')
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class ClientSerializer(serializers.ModelSerializer):
    adresses = AddressNestedSerializer(many=True, required=False)

    class Meta:
        model = apps.get_model('clients', 'Client')
        fields = '__all__'
        read_only_fields = ['utilisateur']

    def validate_raison_sociale(self, value):
        """Check uniqueness per user"""
        request = self.context['request']
        queryset = self.Meta.model.objects.filter(
            utilisateur=request.user,
            raison_sociale=value
        )
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                "You already have a client with this company name."
            )
        return value

    def create(self, validated_data):
        addresses_data = validated_data.pop('adresses', [])
        client = self.Meta.model.objects.create(**validated_data)
        AddressModel = apps.get_model('clients', 'Address')
        for address_data in addresses_data:
            AddressModel.objects.create(client=client, **address_data)
        return client

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('adresses', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if addresses_data is not None:
            AddressModel = apps.get_model('clients', 'Address')
            instance.adresses.all().delete()
            for address_data in addresses_data:
                AddressModel.objects.create(client=instance, **address_data)

        return instance
