from django_filters import rest_framework as filter

from reviews.models import Title


class TitleFilter(filter.FilterSet):
    """Фильтр для модели произведений."""

    genre = filter.CharFilter(field_name='genre__slug')
    category = filter.CharFilter(field_name='category__slug')
    year = filter.NumberFilter()
    name = filter.CharFilter(field_name='name')

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
