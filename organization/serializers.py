from rest_framework import serializers

from organization.models import Organization
from shared.Filters import CustomFilterSet


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            'id',
            'email',
            'name',
            'description',
            'phone',
            'currency',
            'bankAccount',
            'countryCode',
            'line1',
            'city',
            'state',
            'postalCode',
            'web',
            'stripeId',
            'created_at'
        )


class OrganizationFilterSet(CustomFilterSet):
    class Meta:
        model = Organization
        fields = [
            'email',
            'name',
            'description',
            'phone',
            'currency',
            'countryCode',
            'line1',
            'city',
            'state',
            'postalCode',
            'project'
        ]
