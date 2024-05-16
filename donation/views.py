from django.http import JsonResponse
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView

from donation.models import Donation
from donation.serializers import DonationSerializer, CreateDonationSerializer, DonationFilterSet, \
    SimpleDonationSerializer
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
        'create': CreateDonationSerializer,
    }

    @action(methods=['get'], detail=False, url_path='organization/(?P<id>[^/.]+)', url_name="donation_by_organization")
    def donation_by_organization(self, request, id):
        if not id:
            return JsonResponse({"error": "Organization is required"}, status=400)
        donations = Donation.objects.filter(organization_id=id)
        serializer = SimpleDonationSerializer(donations, many=True)
        return JsonResponse(serializer.data, safe=False)
