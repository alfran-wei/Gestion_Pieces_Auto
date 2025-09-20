from django.shortcuts import redirect
from django.contrib import messages

ADMIN_PASSWORD = "12345"

def require_password(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method == "POST":
            password = request.POST.get("password")
            if password != ADMIN_PASSWORD:
                messages.error(request, "Mot de passe incorrect !")
                return redirect(request.META.get("HTTP_REFERER", "/"))
        return view_func(request, *args, **kwargs)
    return wrapper
