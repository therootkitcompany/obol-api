from rest_framework import serializers

from organization.models import Organization
from project.models import Project
from project.serializers import ProjectSerializer
from shared.Filters import CustomFilterSet


class OrganizationSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id',
            'email',
            'name',
            'description',
            'phone',
            'currency',
            'bankAccount',
            'countryCode',
            'line1',
            'city',
            'state',
            'postalCode',
            'web',
            'project',
            'stripeId',
            'created_at'
        )


class OrganizationFilterSet(CustomFilterSet):
    class Meta:
        model = Organization
        fields = [
            'email',
            'name',
            'description',
            'phone',
            'currency',
            'countryCode',
            'line1',
            'city',
            'state',
            'postalCode',
            'project'
        ]


class CreateOrganizationSerializer(serializers.ModelSerializer):
    idProject = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True)

    class Meta:
        model = Organization
        fields = (
            'email',
            'name',
            'description',
            'phone',
            'currency',
            'bankAccount',
            'countryCode',
            'line1',
            'city',
            'state',
            'postalCode',
            'web',
            'idProject',
        )

    def create(self, validated_data):
        project = validated_data.pop('idProject')

        instance = Organization.objects.create(
            project=project,
            **validated_data
        )
        return instance

    def to_representation(self, data):
        return OrganizationSerializer(context=self.context).to_representation(data)
