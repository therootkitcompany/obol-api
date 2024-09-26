from datetime import timedelta

from django.http import JsonResponse
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from charges.models import Charge
from charges.serializers import ChargeSerializer, CreateTokenSerializer
from shared.emailService import send_email
from shared.mixins import DynamicSerializersMixin
from temporaryTokens.models import TemporaryToken


class GenerateTokenViewSet(DynamicSerializersMixin, viewsets.GenericViewSet):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer

    serializer_classes_by_action = {
        'send_token': CreateTokenSerializer
    }

    @action(methods=['post'], detail=False, url_path="send-token", url_name="send_token")
    def send_token(self, request, *args, **kwargs):
        data = CreateTokenSerializer(data=request.data)
        if not data.is_valid():
            return JsonResponse({"error": "Email is required"}, status=400)
        expiration_time = now() + timedelta(hours=1)

        email = data.validated_data.get('email')
        token = TemporaryToken.objects.create(email=email, expires_at=expiration_time)

        send_email(token.token, email)
        return Response({"message": "Token sent to email: " + token.email, "validUntil": token.expires_at},
                        status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path='(?P<email>[^/.@]+@[^\./]+\.[^/.]+)/(?P<id>[^/.]+)', url_name="get_transfers_data")
    def get_transfers_data(self, request, email, id):
        if not id:
            raise ValidationError({"error": "Token is required"}, code=400)
        try:
            savedToken = TemporaryToken.objects.get(token=id)
        except TemporaryToken.DoesNotExist:
            raise ValidationError({"error": "Invalid token"}, code=400)

        if not savedToken.is_valid():
            raise ValidationError({"error": "Token has expired"}, code=400)
        if email != savedToken.email:
            raise ValidationError({"error": "The email provided does not match the token's email"}, code=400)
        charges = Charge.objects.filter(donation__email=savedToken.email)
        serializer = ChargeSerializer(charges, many=True)
        return JsonResponse(serializer.data, safe=False)
