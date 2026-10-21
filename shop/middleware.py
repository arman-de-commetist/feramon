from django.conf import settings
from django.utils import translation


class CookieLanguageMiddleware:
    """Language comes only from the visitor's choice (cookie); Russian by default."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.codes = {code for code, _ in settings.LANGUAGES}

    def __call__(self, request):
        lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if lang not in self.codes:
            lang = settings.LANGUAGE_CODE
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        response.headers.setdefault('Content-Language', lang)
        return response
