from functools import wraps
from django.shortcuts import redirect

def sbt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='SBT').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # Измените на нужное перенаправление
    return _wrapped_view

def spitamen_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.groups.filter(name='Spitamen').exists():
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # Измените на нужное перенаправление
    return _wrapped_view
