def admin_user(request):
    return {
        "admin_user": request.user if request.user.is_authenticated else None
    }
