from rest_framework import serializers

from project.models import Project
from shared.Filters import CustomFilterSet


class ProjectSerializer(serializers.ModelSerializer):
    totalAmount = serializers.SerializerMethodField()
    totalDonations = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'goal', 'status',
            'totalAmount', 'totalDonations', 'progress',
            'commission', 'created_at', 'updated_at', 'endDate'
        ]

    def get_totalAmount(self, obj):
        return obj.totalAmount

    def get_totalDonations(self, obj):
        return obj.totalDonations

    def get_progress(self, obj):
        return obj.progress


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'name',
            'description',
            'goal',
            'status',
            'endDate'
        )


class ProjectFilterSet(CustomFilterSet):
    class Meta:
        model = Project
        fields = [
            'name',
            'status',
        ]
