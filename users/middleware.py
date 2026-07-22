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
            r'^/webprojects/.*/load-files/',
        ]
        
        for pattern in exclude_patterns:
            if re.match(pattern, path):
                return False
        
        return True
    
    def get_client_ip(self, request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
    
    def get_device_type(self, user_agent):
        """Detect device type from user agent"""
        if not user_agent:
            return 'unknown'
        ua = user_agent.lower()
        if 'mobile' in ua or 'android' in ua or 'iphone' in ua:
            return 'mobile'
        elif 'tablet' in ua or 'ipad' in ua:
            return 'tablet'
        return 'desktop'
    
    def get_browser(self, user_agent):
        """Detect browser from user agent"""
        if not user_agent:
            return 'unknown'
        ua = user_agent.lower()
        if 'firefox' in ua:
            return 'Firefox'
        elif 'chrome' in ua and 'edg' not in ua:
            return 'Chrome'
        elif 'edg' in ua:
            return 'Edge'
        elif 'safari' in ua and 'chrome' not in ua:
            return 'Safari'
        elif 'opera' in ua:
            return 'Opera'
        return 'Other'
    
    def get_os(self, user_agent):
        """Detect operating system from user agent"""
        if not user_agent:
            return 'unknown'
        ua = user_agent.lower()
        if 'windows' in ua:
            return 'Windows'
        elif 'mac' in ua:
            return 'MacOS'
        elif 'linux' in ua and 'android' not in ua:
            return 'Linux'
        elif 'android' in ua:
            return 'Android'
        elif 'iphone' in ua or 'ipad' in ua:
            return 'iOS'
        return 'Other'
    
    def process_request(self, request):
        """Track visit on each request - with error handling"""
        
        if not self.should_track(request):
            return None
        
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
    

class UpdateLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            skip_paths = [r'^/static/', r'^/media/', r'^/admin/', r'^/webprojects/file-autosave/', r'^/webprojects/.*/chat/', r'^/webprojects/.*/load-files/', r'\.json$', r'\.xml$']
            should_skip = any(re.match(p, request.path) for p in skip_paths)
            if not should_skip:
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    now = timezone.now()
                    User.objects.filter(id=request.user.id).update(last_activity=now)
                    request.user.last_activity = now
                except Exception as e:
                    logger.warning(f"LastActivity update failed: {e}")
        return self.get_response(request)