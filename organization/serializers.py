from rest_framework import serializers

from organization.models import Organization
from shared.Filters import CustomFilterSet


class OrganizationSerializer(serializers.ModelSerializer):
    bankAccount = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            'id',
            'email',
            'name',
            'description',
            'phone',
            'bankAccount',
            'created_at',
            'updated_at',
        )

    def get_bankAccount(self, obj: Organization):
        return obj.mask_bankAccount()


class OrganizationFilterSet(CustomFilterSet):
    class Meta:
        model = Organization
        fields = [
            'email',
            'name',
            'description',
            'phone',
        ]
