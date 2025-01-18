import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Course, Lesson, Subscription
from .serializers import (
    CourseWithLessonsSerializer,
    LessonSerializer,
    SubscriptionSerializer,
)
from .permissions import IsOwnerOrModerator  # Кастомное разрешение для проверки прав доступа
from .paginators import CoursePagination, LessonPagination  # Импорт пагинаторов

# Настройка ключа API Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    pagination_class = CoursePagination  # Использование пагинатора для курсов
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Привязываем курс к текущему пользователю


class CourseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def get_queryset(self):
        return Course.objects.filter(user=self.request.user)


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination  # Использование пагинатора для уроков
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.user != self.request.user:
            raise PermissionDenied("You do not have permission to add lessons to this course.")
        serializer.save(user=self.request.user)  # Привязываем урок к текущему пользователю


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]  # Доступ только для владельцев и модераторов

    def get_queryset(self):
        return Lesson.objects.filter(user=self.request.user)


class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


# Новый View для создания сессии оплаты через Stripe
class CreateCheckoutSessionView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        YOUR_DOMAIN = settings.FRONTEND_URL

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Course Subscription',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )

        return JsonResponse({'id': checkout_session.id})


# Новый View для создания цены для продукта через Stripe
class CreatePriceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        price_amount = request.data.get('price_amount')

        if not product_id or not price_amount:
            return JsonResponse({'error': 'Product ID and price amount are required'}, status=400)

        try:
            # Создаем цену для продукта через Stripe
            price = stripe.Price.create(
                unit_amount=int(price_amount) * 100,  # Преобразуем в центы
                currency='usd',
                product=product_id,
            )

            return JsonResponse({
                'id': price.id,
                'unit_amount': price.unit_amount,
                'currency': price.currency,
            })

        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)


# Новый View для обработки webhook от Stripe
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )

    except ValueError as e:

        return JsonResponse({'message': 'Invalid payload'}, status=400)

    except stripe.error.SignatureVerificationError as e:

        return JsonResponse({'message': 'Invalid signature'}, status=400)

    # Обработка события
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        user_email = session.get('customer_email')

        print(f"Payment successful for {user_email}")

    return JsonResponse({'status': 'success'})
