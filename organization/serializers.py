from rest_framework import serializers

from organization.models import Organization
from project.serializers import ProjectSerializer
from shared.Filters import CustomFilterSet


class OrganizationSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
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
            'project',
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
