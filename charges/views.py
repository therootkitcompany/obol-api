from datetime import timedelta

from django.http import JsonResponse
from django.utils.timezone import now
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

    @action(methods=['post'], detail=False, url_name="send_token")
    def send_token(self, request, *args, **kwargs):
        data = CreateTokenSerializer(data=request.data)
        if not data.is_valid():
            return JsonResponse({"error": "Email is required"}, status=400)
        expiration_time = now() + timedelta(hours=1)

        email = data.validated_data.get('email')
        token = TemporaryToken.objects.create(email=email, expires_at=expiration_time)

        send_email(request, token.token, email)
        return Response({"message": "Token sent to email: " + token.email, "validUntil": token.expires_at},
                        status=status.HTTP_201_CREATED)

    serializer_classes_by_action = {
        'send_token': CreateTokenSerializer
    }
