from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def role_required(*allowed_roles):
    """
    Decorator to check if user has required role
    Usage: @role_required('admin', 'teacher')
    """
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            # Check if user has a profile
            if not hasattr(request.user, 'profile'):
                messages.error(request, "User profile not found. Please contact admin.")
                return redirect('index')
            
            user_role = request.user.profile.role
            
            if user_role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('index')
        
        return wrapper
    return decorator