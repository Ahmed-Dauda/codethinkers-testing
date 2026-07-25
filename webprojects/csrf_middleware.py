class SubdomainCSRFMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow all subdomains of codethinkers.org
        origin = request.META.get('HTTP_ORIGIN', '')
        if origin and '.codethinkers.org' in origin:
            # Add to trusted origins dynamically
            from django.conf import settings
            trusted = list(getattr(settings, 'CSRF_TRUSTED_ORIGINS', []))
            if origin not in trusted:
                trusted.append(origin)
                settings.CSRF_TRUSTED_ORIGINS = trusted
        return self.get_response(request)
