import stripe
from django.conf import settings
from django.http import JsonResponse
from courses.models import Subscription, Course

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = 'whsec_...'
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)

    # Обработка события
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_email = session['customer_details']['email']
        course_id = session['metadata']['course_id']

        # Добавляем подписку
        course = Course.objects.get(id=course_id)
        Subscription.objects.create(user__email=user_email, course=course)

    return JsonResponse({'status': 'success'}, status=200)
