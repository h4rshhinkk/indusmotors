# middleware.py
from django.contrib.auth import logout
from django.utils import timezone


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is authenticated
        if request.user.is_authenticated:
            last_activity_str = request.session.get("last_activity")

            # If last_activity is not set, set it to the current time
            if not last_activity_str:
                request.session["last_activity"] = str(timezone.now())
            else:
                # Convert last_activity to a datetime object
                last_activity = timezone.datetime.fromisoformat(last_activity_str)

                # Check if the user has been inactive for more than 1 minute
                if (timezone.now() - last_activity).seconds > 3600:
                    logout(request)
                else:
                    # Update last_activity for the next request
                    request.session["last_activity"] = str(timezone.now())

        return response
