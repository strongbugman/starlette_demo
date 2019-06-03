from sentry_asgi import SentryMiddleware as _SentryMiddleware
import sentry_sdk

import settings


class SentryMiddleware(_SentryMiddleware):
    def __init__(self, app):
        sentry_sdk.init(settings.DSN)
        super().__init__(app)
