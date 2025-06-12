

import logging
from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('request_logger')

        if not self.logger.handlers:
            handler = logging.FileHandler('user_requests.log')
            formatter = logging.Formatter('%(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)

        response = self.get_response(request)
        return response

from datetime import datetime, time
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start_allowed = time(18, 0)  
        end_allowed = time(21, 0)    

        # Check if the request path is targeting the messaging app
        if request.path.startswith('/api/chats/'):
            if not (start_allowed <= current_time <= end_allowed):
                return HttpResponseForbidden("Access to messaging is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)
# core/middleware.py

from datetime import datetime, timedelta
from django.http import JsonResponse

class OffensiveLanguageMiddleware:
    """
    Middleware to rate-limit chat messages per IP address.
    Restricts users to 5 messages per minute to prevent spam.
    """

    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response
        self.message_logs = {}  # Store: {ip: [timestamp1, timestamp2, ...]}

    def __call__(self, request):
        """
        Handles each request and enforces the rate limit on POSTs to /api/chats/messages/.

        Returns:
            - 403 response if the limit is exceeded
            - Otherwise, passes to the next middleware/view
        """
        # Apply rate limiting only to chat message creation endpoint
        if request.path.startswith('/api/chats/messages/') and request.method == 'POST':
            ip = self.get_client_ip(request)
            now = datetime.now()
            window = timedelta(minutes=1)

            # Get timestamps for this IP, filter to only those within the last 1 minute
            timestamps = self.message_logs.get(ip, [])
            timestamps = [ts for ts in timestamps if now - ts < window]

            if len(timestamps) >= 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded. Max 5 messages per minute."},
                    status=403
                )

            # Log this request's timestamp
            timestamps.append(now)
            self.message_logs[ip] = timestamps

        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Extract the client IP address from the request.

        Returns:
            str: The client's IP address.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
    """
    Middleware to restrict access based on user roles.
    Only users with 'admin' or 'moderator' role can access protected views.
    """

    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Intercepts incoming requests and checks if the user has permission
        to access protected routes based on their role.
        """

        # Example: Restrict access to any URL starting with /admin-only/
        if request.path.startswith('/admin-only/'):
            user = request.user

            # If user is not authenticated or doesn't have the right role
            if not user.is_authenticated:
                return HttpResponseForbidden("Access denied: Login required.")
            
            # You can change these role checks based on your model structure
            user_role = getattr(user, 'role', None)  # assumes 'role' is a field on your user model

            if user_role not in ['admin', 'moderator']:
                return HttpResponseForbidden("Access denied: Insufficient role privileges.")

        # Allow request to proceed if not blocked
        return self.get_response(request)
