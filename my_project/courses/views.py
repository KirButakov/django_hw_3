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
from .permissions import IsOwnerOrModerator
from .paginators import CoursePagination, LessonPagination
from django.core.mail import send_mail

# Настройка ключа API Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    pagination_class = CoursePagination
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithLessonsSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def perform_update(self, serializer):
        instance = serializer.save()
        self.notify_subscribers(instance)

    def notify_subscribers(self, course):
        subscribers = Subscription.objects.filter(course=course).select_related('user')
        for subscription in subscribers:
            self.send_update_notification(course, subscription.user.email)

    def send_update_notification(self, course, user_email):
        send_mail(
            subject=f"Обновление курса {course.name}",
            message=f"Курс {course.name} был обновлен. Проверьте новые материалы!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
        )


class LessonListCreateView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.user != self.request.user:
            raise PermissionDenied("You do not have permission to add lessons to this course.")
        serializer.save(user=self.request.user)


class LessonRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrModerator]

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


class CreatePriceView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        price_amount = request.data.get('price_amount')

        if not product_id or not price_amount:
            return JsonResponse({'error': 'Product ID and price amount are required'}, status=400)

        try:
            price = stripe.Price.create(
                unit_amount=int(price_amount) * 100,
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

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session.get('customer_email')
        print(f"Payment successful for {user_email}")

    return JsonResponse({'status': 'success'})
