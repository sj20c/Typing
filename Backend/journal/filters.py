import django_filters
from .models import HappyMoment


class HappyMomentFilter(django_filters.FilterSet):
    from_date = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    to_date = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    tag = django_filters.CharFilter(method="filter_tag")

    class Meta:
        model = HappyMoment
        fields = ["from_date", "to_date", "tag"]

    def filter_tag(self, queryset, name, value):
        # tags 배열에 value 포함된 것만
        return queryset.filter(tags__contains=[value])
