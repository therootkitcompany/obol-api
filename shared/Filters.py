from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.filters import OrderingFilter


class CustomFilterSet(filters.FilterSet):
    quantity = filters.NumberFilter(method='filter_quantity')
    direction = filters.CharFilter(method='filter_direction')
    order = OrderingFilter()

    def filter_quantity(self, queryset, name, value):
        quantity_value = int(value)
        return queryset[:quantity_value] if quantity_value >= 0 else queryset

    def filter_direction(self, queryset, name, value):
        if value.lower() == 'asc':
            return queryset.order_by(self.data['order'])
        elif value.lower() == 'desc':
            return queryset.order_by(f'-{self.data["order"]}')
        else:
            return queryset

    class Meta:
        fields = []


class GenericViewSetWithFilters(mixins.ListModelMixin, viewsets.GenericViewSet):
    filterset_class = None

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.filterset_class:
            filterset = self.filterset_class(self.request.GET, queryset=queryset)
            queryset = filterset.qs
        return queryset

    @classmethod
    def get_ordering_fields(cls, model):
        return [(field.name, field.name.capitalize()) for field in model._meta.get_fields() if hasattr(field, 'name')]

    def get_filterset_class(self):
        if self.filterset_class:
            ordering_fields = self.get_ordering_fields(self.filterset_class.Meta.model)
            self.filterset_class.base_filters['order'].extra['choices'] = ordering_fields
        return self.filterset_class
