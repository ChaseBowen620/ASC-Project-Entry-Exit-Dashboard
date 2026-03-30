from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Try Authorization header first, then the httpOnly access token cookie.
    """

    def authenticate(self, request):
        header = self.get_header(request)
        if header is not None:
            return super().authenticate(request)
        raw = request.COOKIES.get(settings.JWT_AUTH_COOKIE)
        if not raw:
            return None
        validated_token = self.get_validated_token(raw)
        return self.get_user(validated_token), validated_token
