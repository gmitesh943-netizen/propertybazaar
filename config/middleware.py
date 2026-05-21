"""Dev-only helpers for tunnel URLs (LocalTunnel, ngrok)."""


class TunnelCSRFMiddleware:
    """Allow CSRF from any *.loca.lt host when DEBUG is on."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings

        if settings.DEBUG:
            host = request.get_host().split(':')[0]
            for suffix in ('.loca.lt', '.localtunnel.me', '.ngrok-free.app', '.ngrok.io'):
                if host.endswith(suffix):
                    origin = f'https://{request.get_host()}'
                    if origin not in settings.CSRF_TRUSTED_ORIGINS:
                        settings.CSRF_TRUSTED_ORIGINS.append(origin)
                    break

        return self.get_response(request)
