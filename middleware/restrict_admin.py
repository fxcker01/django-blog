from django.http import HttpResponseForbidden

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/admin') and not request.user.is_staff:
            return HttpResponseForbidden("403 Forbidden: Access denied.")
        return self.get_response(request)