from django.shortcuts import redirect
from functools import wraps

def admin_required(view_func):
    """Décorateur : seuls les admins et superusers peuvent accéder à cette vue."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper

def admin_or_teacher_required(view_func):
    """Décorateur : admins, superusers ET teachers peuvent accéder à cette vue."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser or request.user.is_teacher
        ):
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper
