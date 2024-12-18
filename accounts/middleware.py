# accounts/middleware.py
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse

class RestrictBackAfterLogoutMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        # Update the logout path to the correct one for your project
        logout_path = '/CGS_Records/logout/'  # Change this to your actual logout path

        # Check if the user is authenticated and is accessing the logout URL
        if request.user.is_authenticated and request.path == logout_path:
            # Logic to prevent back navigation after logout
            return redirect('accounts:home_login')  # Redirect to your desired URL

        # Define protected URLs
        protected_urls = [
            '/CGS_Records/base/',
            '/CGS_Records/masteral_page/', 
            '/CGS_Records/doctoral_page/', 
            '/CGS_Records/faculty_page/'
            '/CGS_Dashboard/dashboard/'
        ]
        
        # Redirect to login if user is not authenticated and accessing protected URLs
        if not request.user.is_authenticated and request.path in protected_urls:
            return redirect(reverse('accounts:home_login'))  # Redirect to the login page if user is logged out

        # Call the next middleware or view
        response = self.get_response(request)
        return response
