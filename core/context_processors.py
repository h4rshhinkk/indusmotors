from django.conf import settings


def main_context(request):
    current_employee = None
    name = None
    app_settings = settings.APP_SETTINGS

    if request.user.is_authenticated:
        current_employee = request.user
        name = current_employee.first_name

    return {
        "current_employee": current_employee,
        "default_user_avatar": f"https://ui-avatars.com/api/?name={name}&background=e9ebfa&color=fff&size=128",
        "app_settings": app_settings,
        "current_version": "?v=2.1",
    }
