# middleware.py

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from .models import UserVisit, PageView
from datetime import timedelta
import re
import logging

logger = logging.getLogger(__name__)

# ✅ Import your custom user model
from django.contrib.auth import get_user_model
User = get_user_model()  # This gets your NewUser model


class VisitTrackingMiddleware(MiddlewareMixin):
    # ... (keep all your existing code, but update the should_track method)
    
    def should_track(self, request):
        """Determine if this request should be tracked"""
        path = request.path
        exclude_patterns = [
            r'^/static/',
            r'^/media/',
            r'^/admin/',
            r'^/api/',
            r'\.json$',
            r'\.xml$',
            r'\.ico$',
            r'^/webprojects/file-autosave/',
            r'^/webprojects/.*/chat/',
            r'^/webprojects/.*/load-files/',  # ✅ Also skip load-files
        ]
        
        for pattern in exclude_patterns:
            if re.match(pattern, path):
                return False
        
        return True
    
    # ... rest of your methods (get_client_ip, get_device_type, etc.)
    
    def process_request(self, request):
        """Track visit on each request - with error handling"""
        
        if not self.should_track(request):
            return None
        
        # ✅ Only track authenticated users to reduce load
        if not request.user.is_authenticated:
            return None
        
        try:
            now = timezone.now()
            session_key = request.session.session_key
            
            if not session_key:
                request.session.save()
                session_key = request.session.session_key
            
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            ip_address = self.get_client_ip(request)
            device_type = self.get_device_type(user_agent)
            browser = self.get_browser(user_agent)
            os = self.get_os(user_agent)
            
            # Get or create visit
            visit = None
            try:
                visit = UserVisit.objects.filter(
                    user=request.user,
                    session_key=session_key,
                    last_activity__gte=now - timedelta(minutes=30)
                ).first()
            except Exception as e:
                logger.warning(f"Visit lookup failed: {e}")
                return None
            
            if visit:
                try:
                    UserVisit.objects.filter(id=visit.id).update(
                        last_activity=now,
                        page_views=visit.page_views + 1
                    )
                except Exception as e:
                    logger.warning(f"Visit update failed: {e}")
            else:
                try:
                    visit = UserVisit.objects.create(
                        user=request.user,
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
                except Exception as e:
                    logger.warning(f"Visit creation failed: {e}")
                    return None
            
            if visit:
                try:
                    PageView.objects.create(
                        visit=visit,
                        url=request.build_absolute_uri(),
                        timestamp=now
                    )
                except Exception as e:
                    logger.warning(f"PageView creation failed: {e}")
            
            request.visit_id = visit.id if visit else None
            
        except Exception as e:
            logger.error(f"VisitTrackingMiddleware error: {e}")
        
        return None


class BotSignupProtectionMiddleware(MiddlewareMixin):
    def __call__(self, request):
        if request.path == '/accounts/signup/' and request.method == 'GET':
            request.session['form_created_at'] = timezone.now().isoformat()
        return super().__call__(request)


class UpdateLastActivityMiddleware:
    """
    Middleware to update user last_activity - with rate limiting
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # ✅ Only update if user is authenticated
        if request.user.is_authenticated:
            # Skip for certain paths
            path = request.path
            skip_paths = [
                r'^/static/',
                r'^/media/',
                r'^/admin/',
                r'^/webprojects/file-autosave/',
                r'^/webprojects/.*/chat/',
                r'^/webprojects/.*/load-files/',  # ✅ Skip load-files
                r'\.json$',
                r'\.xml$',
            ]
            
            should_skip = False
            for pattern in skip_paths:
                if re.match(pattern, path):
                    should_skip = True
                    break
            
            if not should_skip:
                try:
                    now = timezone.now()
                    # ✅ Use the User model (which is NewUser)
                    User.objects.filter(id=request.user.id).update(
                        last_activity=now
                    )
                    # Update the user object in memory
                    request.user.last_activity = now
                except Exception as e:
                    logger.warning(f"LastActivity update failed: {e}")
        
        return self.get_response(request)