# context_processors.py (create this file in your webprojects app)
from .models import PlatformSettings

def platform_settings(request):
    return {
        'platform_settings': PlatformSettings.get_settings(),
    }