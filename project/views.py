from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView

from donation.serializers import CreateDonationSerializer
from project.models import Project
from project.serializers import ProjectSerializer, ProjectFilterSet
from rest_framework import mixins
from shared.Filters import GenericViewSetWithFilters
from shared.mixins import DynamicSerializersMixin, APIKeyPermission
from django_filters import rest_framework as filters


@extend_schema_view(
    list=extend_schema(description='Get paginated list of project.'),
    create=extend_schema(description='Create a new project.', responses={200: ProjectSerializer}),
    destroy=extend_schema(description='Delete a project.'),
    update=extend_schema(description='Update a project.'),
)
class ProjectViewSet(DynamicSerializersMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSetWithFilters, RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilterSet
    filter_backends = (filters.DjangoFilterBackend,)

    serializer_classes_by_action = {
        'create': CreateDonationSerializer,
    }

    # def get_permissions(self):
    #     return [APIKeyPermission()]
