from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.generics import RetrieveAPIView

from donation.models import Donation
from donation.serializers import DonationSerializer, CreateDonationSerializer, DonationFilterSet
from shared.Filters import GenericViewSetWithFilters
from shared.mixins import DynamicSerializersMixin
from django_filters import rest_framework as filters


@extend_schema_view(
    list=extend_schema(description='Get paginated list of donations.'),
    create=extend_schema(description='Create a new donation.', responses={200: DonationSerializer}),
)
class DonationViewSet(DynamicSerializersMixin, mixins.CreateModelMixin, GenericViewSetWithFilters, RetrieveAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    filterset_class = DonationFilterSet
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_classes_by_action = {
        'create': CreateDonationSerializer
    }
