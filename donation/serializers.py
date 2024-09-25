from rest_framework import serializers

from donation.models import Donation
from organization.models import Organization
from organization.serializers import OrganizationSerializer
from shared.Filters import CustomFilterSet


class SimpleDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = (
            'id',
            'email',
            'name',
            'created_at',
            'updated_at',
            'amount',
            'currency',
            'country',
            'city'
        )


class DonationSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Donation
        fields = (
            'id',
            'email',
            'name',
            'organization',
            'created_at',
            'updated_at',
            'amount',
            'currency',
            'country',
            'city'
        )


class CreateDonationSerializer(serializers.ModelSerializer):
    idOrganization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), write_only=True)
    organization = OrganizationSerializer(read_only=True)
    stripeSessionId = serializers.CharField(write_only=True)

    class Meta:
        model = Donation
        fields = (
            'stripeSessionId',
            'idOrganization',
            'organization'
        )

    def create(self, validated_data):
        organization = validated_data.pop('idOrganization')

        instance = Donation.objects.create(
            organization=organization,
            **validated_data
        )
        return instance

    def to_representation(self, data):
        return DonationSerializer(context=self.context).to_representation(data)


class DonationFilterSet(CustomFilterSet):
    class Meta:
        model = Donation
        fields = [
            'email',
            'name',
            'amount',
            'currency',
            'country',
            'city'
        ]
