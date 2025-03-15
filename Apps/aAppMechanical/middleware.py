from .models import aLogEntry
from django.utils.timezone import now

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            aLogEntry.objects.create(
                user=request.user,
                message=f"at {now()} Accessed {request.path} "
            )

        return response
