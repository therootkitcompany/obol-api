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
            'created_at',
            'updated_at',
        )


class OrganizationFilterSet(CustomFilterSet):
    class Meta:
        model = Organization
        fields = [
            'email',
            'name',
            'description',
            'phone',
        ]
