import requests
from django.http import JsonResponse
from django.conf import settings

class ExternalTokenMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.bypass_urls = ['/api/auth/login/', '/api/auth/verify/', '/admin/']

    def __call__(self, request):
        # 1. Check if URL should be bypassed
        if any(request.path.startswith(url) for url in self.bypass_urls):
            return self.get_response(request)

        # 2. Get token from header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'No Authorization header'}, status=401)

        # 3. Hit the internal auth/verify API
        try:
            # Note: Adjust URL to your internal service if separate
            verify_url = "http://0.0.0.0:8000/auth/verify/" 
            response = requests.post(verify_url, headers={'Authorization': auth_header})
            
            if response.status_code != 200:
                return JsonResponse({'error': 'Invalid Token'}, status=401)
        except requests.RequestException:
            return JsonResponse({'error': 'Auth service unavailable'}, status=503)

        return self.get_response(request)