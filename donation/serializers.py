from rest_framework import serializers

from donation.models import Donation
from shared.Filters import CustomFilterSet


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = (
            'id',
            'email',
            'name',
            'surname',
            'created_at',
            'updated_at',
            'amount',
            'status',
            'country',
            'city'
        )


class CreateDonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = (
            'email',
            'name',
            'surname',
            'amount'
        )

    def create(self, validated_data):
        status: str = 'Pending'

        instance = Donation.objects.create(
            status=status,
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
            'surname',
            'amount',
        ]
