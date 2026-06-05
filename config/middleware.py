from django.utils.timezone import now
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse

class SessionIdleTimeoutMiddleware:
    """Middleware to log out inactive users after 5 minutes"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Skip for non-authenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Get last activity timestamp from session
        last_activity = request.session.get('last_activity')
        current_time = now().timestamp()
        
        if last_activity:
            # Check if idle time exceeds 5 minutes
            idle_time = current_time - last_activity
            if idle_time > 300:  # 5 minutes
                logout(request)
                # Optional: Add a message
                from django.contrib import messages
                messages.warning(request, 'You have been logged out due to inactivity.')
                # Don't continue processing
                return redirect(reverse('login'))
        
        # Update last activity timestamp
        request.session['last_activity'] = current_time
        
        return self.get_response(request)