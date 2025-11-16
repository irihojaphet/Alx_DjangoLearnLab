"""
Custom middleware for security enhancements.

This module provides middleware for adding Content Security Policy (CSP) headers
and other security-related HTTP headers.
"""

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class CSPMiddleware(MiddlewareMixin):
    """
    Middleware to add Content Security Policy (CSP) headers.
    
    CSP helps prevent XSS attacks by specifying which domains are allowed
    to load resources (scripts, styles, images, etc.) in your application.
    
    This middleware reads CSP settings from Django settings and adds the
    appropriate CSP header to all responses.
    """
    
    def process_response(self, request, response):
        """
        Add Content Security Policy header to the response.
        
        Reads CSP settings from Django settings and constructs the CSP header.
        If CSP settings are not configured, this middleware does nothing.
        """
        csp_directives = []
        
        # Build CSP directives from settings
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_directives.append(f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}")
        
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            csp_directives.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
        
        if hasattr(settings, 'CSP_STYLE_SRC'):
            csp_directives.append(f"style-src {' '.join(settings.CSP_STYLE_SRC)}")
        
        if hasattr(settings, 'CSP_IMG_SRC'):
            csp_directives.append(f"img-src {' '.join(settings.CSP_IMG_SRC)}")
        
        if hasattr(settings, 'CSP_FONT_SRC'):
            csp_directives.append(f"font-src {' '.join(settings.CSP_FONT_SRC)}")
        
        # Add CSP header if directives are configured
        if csp_directives:
            response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        return response

