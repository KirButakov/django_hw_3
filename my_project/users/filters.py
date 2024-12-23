import django_filters
from .models import Payment

class PaymentFilter(django_filters.FilterSet):
    date_from = django_filters.DateTimeFilter(field_name="payment_date", lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name="payment_date", lookup_expr='lte')
    paid_course = django_filters.NumberFilter(field_name="paid_course")
    paid_lesson = django_filters.NumberFilter(field_name="paid_lesson")
    payment_method = django_filters.CharFilter(field_name="payment_method", lookup_expr='iexact')

    class Meta:
        model = Payment
        fields = ['date_from', 'date_to', 'paid_course', 'paid_lesson', 'payment_method']
