import time
from django.core.cache import cache
from django.http import HttpResponseForbidden

class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path == '/contato/':
            ip = request.META.get('REMOTE_ADDR')
            key = f'rate_limit_{ip}'
            last_request_time = cache.get(key)
            current_time = time.time()

            if last_request_time and current_time - last_request_time < 300:  # 1 minuto
                return HttpResponseForbidden("Você está enviando solicitações muito rapidamente. Tente novamente mais tarde.")

            cache.set(key, current_time, timeout=300)  # 1 minuto

        response = self.get_response(request)
        return response