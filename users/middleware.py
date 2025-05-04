# middleware.py
from django.utils import timezone

from django.utils.deprecation import MiddlewareMixin

class BotSignupProtectionMiddleware(MiddlewareMixin):
    def __call__(self, request):
        if request.path == '/accounts/signup/' and request.method == 'GET':
            request.session['form_created_at'] = timezone.now().isoformat()
        return super().__call__(request)

