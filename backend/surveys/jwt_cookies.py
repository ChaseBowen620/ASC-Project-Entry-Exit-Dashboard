"""httpOnly cookie helpers for JWT access / refresh tokens."""

from django.conf import settings


def _cookie_options():
    opts = {
        'path': settings.JWT_COOKIE_PATH,
        'httponly': True,
        'secure': settings.JWT_COOKIE_SECURE,
        'samesite': settings.JWT_COOKIE_SAMESITE,
    }
    domain = getattr(settings, 'JWT_COOKIE_DOMAIN', None)
    if domain:
        opts['domain'] = domain
    return opts


def set_jwt_cookies(response, access_token, refresh_token=None):
    """Attach access token cookie; refresh cookie only if refresh_token is not None."""
    jwt_settings = settings.SIMPLE_JWT
    access_max = int(jwt_settings['ACCESS_TOKEN_LIFETIME'].total_seconds())
    opts = _cookie_options()
    response.set_cookie(
        settings.JWT_AUTH_COOKIE,
        access_token,
        max_age=access_max,
        **opts,
    )
    if refresh_token is not None:
        refresh_max = int(jwt_settings['REFRESH_TOKEN_LIFETIME'].total_seconds())
        response.set_cookie(
            settings.JWT_AUTH_REFRESH_COOKIE,
            refresh_token,
            max_age=refresh_max,
            **opts,
        )


def clear_jwt_cookies(response):
    """Remove JWT cookies (same path/domain as when set)."""
    opts = _cookie_options()
    domain = opts.pop('domain', None)
    for name in (settings.JWT_AUTH_COOKIE, settings.JWT_AUTH_REFRESH_COOKIE):
        response.delete_cookie(name, path=opts['path'], domain=domain)
