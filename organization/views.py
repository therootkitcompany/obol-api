from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView

from organization.models import Organization
from organization.serializers import OrganizationSerializer, OrganizationFilterSet
from shared.Filters import GenericViewSetWithFilters
from shared.mixins import DynamicSerializersMixin

from django_filters import rest_framework as filters


@extend_schema_view(
    list=extend_schema(description='Get paginated list of organizations.'),
)
class OrganizationViewSet(DynamicSerializersMixin, GenericViewSetWithFilters, RetrieveAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilterSet
    filter_backends = (filters.DjangoFilterBackend,)
