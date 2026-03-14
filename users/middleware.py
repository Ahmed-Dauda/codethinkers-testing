# In middleware.py (create this file in your app)

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import UserVisit, PageView
from datetime import timedelta
import re

class VisitTrackingMiddleware(MiddlewareMixin):
    """
    Middleware to track user visits and page views
    """
    
    def get_client_ip(self, request):
        """Get real IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_device_type(self, user_agent):
        """Detect device type from user agent"""
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower:
            return 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'tablet'
        elif any(x in user_agent_lower for x in ['windows', 'mac', 'linux']):
            return 'desktop'
        return 'unknown'
    
    def get_browser(self, user_agent):
        """Extract browser name from user agent"""
        if 'chrome' in user_agent.lower():
            return 'Chrome'
        elif 'firefox' in user_agent.lower():
            return 'Firefox'
        elif 'safari' in user_agent.lower() and 'chrome' not in user_agent.lower():
            return 'Safari'
        elif 'edge' in user_agent.lower():
            return 'Edge'
        elif 'opera' in user_agent.lower():
            return 'Opera'
        return 'Unknown'
    
    def get_os(self, user_agent):
        """Extract OS from user agent"""
        user_agent_lower = user_agent.lower()
        if 'windows' in user_agent_lower:
            return 'Windows'
        elif 'mac' in user_agent_lower:
            return 'macOS'
        elif 'linux' in user_agent_lower:
            return 'Linux'
        elif 'android' in user_agent_lower:
            return 'Android'
        elif 'ios' in user_agent_lower or 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
            return 'iOS'
        return 'Unknown'
    
    def should_track(self, request):
        """Determine if this request should be tracked"""
        # Don't track static files, media, admin, or API calls
        path = request.path
        exclude_patterns = [
            r'^/static/',
            r'^/media/',
            r'^/admin/',
            r'^/api/',  # if you have API endpoints
            r'\.json$',
            r'\.xml$',
            r'\.ico$',
        ]
        
        for pattern in exclude_patterns:
            if re.match(pattern, path):
                return False
        
        return True
    
    def process_request(self, request):
        """Track visit on each request"""
        
        if not self.should_track(request):
            return None
        
        now = timezone.now()
        session_key = request.session.session_key
        
        # Get or create session key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        
        # Get user agent info
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        ip_address = self.get_client_ip(request)
        device_type = self.get_device_type(user_agent)
        browser = self.get_browser(user_agent)
        os = self.get_os(user_agent)
        
        # Get or create visit for this session
        visit = None
        
        # Try to find existing active visit (within last 30 minutes)
        if request.user.is_authenticated:
            visit = UserVisit.objects.filter(
                user=request.user,
                session_key=session_key,
                last_activity__gte=now - timedelta(minutes=30)
            ).first()
        else:
            visit = UserVisit.objects.filter(
                session_key=session_key,
                last_activity__gte=now - timedelta(minutes=30)
            ).first()
        
        if visit:
            # Update existing visit
            visit.update_activity()
        else:
            # Create new visit
            visit = UserVisit.objects.create(
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip_address,
                user_agent=user_agent,
                session_key=session_key,
                entry_page=request.build_absolute_uri(),
                referrer=request.META.get('HTTP_REFERER', ''),
                device_type=device_type,
                browser=browser,
                os=os,
                visit_time=now,
                last_activity=now
            )
        
        # Track individual page view
        PageView.objects.create(
            visit=visit,
            url=request.build_absolute_uri(),
            timestamp=now
        )
        
        # Store visit ID in request for later use
        request.visit_id = visit.id
        
        return None


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

