from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView

from rest_framework import mixins

from organization.models import Organization
from organization.serializers import OrganizationSerializer, OrganizationFilterSet, CreateOrganizationSerializer
from shared.Filters import GenericViewSetWithFilters
from shared.mixins import DynamicSerializersMixin, APIKeyPermission

from django_filters import rest_framework as filters


@extend_schema_view(
    list=extend_schema(description='Get paginated list of organizations.'),
    destroy=extend_schema(description='Delete a Organization.'),
    create=extend_schema(description='Create a new organization.', responses={200: OrganizationSerializer}),
)
class OrganizationViewSet(DynamicSerializersMixin, mixins.CreateModelMixin, GenericViewSetWithFilters, RetrieveAPIView,
                          mixins.DestroyModelMixin, ):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filterset_class = OrganizationFilterSet
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_classes_by_action = {
        'create': CreateOrganizationSerializer,
    }

    def get_permissions(self):
        if self.action == 'destroy' or self.action == 'create':
            return [APIKeyPermission()]
        return super().get_permissions()
