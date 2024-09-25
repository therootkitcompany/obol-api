from rest_framework import serializers

from charges.models import Charge
from donation.serializers import SimpleDonationSerializer
from temporaryTokens.models import TemporaryToken


class SimpleChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = (
            'id',
            'status',
            'receiptUrl',
            'paymentMethod',
            'transferId',
            'chargeId',
            'amountReceived',
            'applicationFee',
            'currency',
            'description',
            'created_at',
            'updated_at'
        )


class ChargeSerializer(serializers.ModelSerializer):
    donation = SimpleDonationSerializer(read_only=True)

    class Meta:
        model = Charge
        fields = (
            'id',
            'status',
            'receiptUrl',
            'paymentMethod',
            'transferId',
            'chargeId',
            'amountReceived',
            'applicationFee',
            'currency',
            'description',
            'donation',
            'created_at',
            'updated_at'
        )


class CreateTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
