# middleware.py
from django.utils import timezone

from django.utils.deprecation import MiddlewareMixin

class BotSignupProtectionMiddleware(MiddlewareMixin):
    def __call__(self, request):
        if request.path == '/accounts/signup/' and request.method == 'GET':
            request.session['form_created_at'] = timezone.now().isoformat()
        return super().__call__(request)

from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

from django.utils.timezone import now

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = now()
            request.user.save(update_fields=["last_activity"])
        return self.get_response(request)

