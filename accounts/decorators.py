from django.contrib.auth.decorators import user_passes_test


def staff_required(view_func=None):
    decorator = user_passes_test(
        lambda user: user.is_authenticated and user.is_staff,
        login_url="login",
    )
    if view_func:
        return decorator(view_func)
    return decorator
