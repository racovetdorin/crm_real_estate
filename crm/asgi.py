"""
ASGI config for crm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import sentry_sdk
from django.conf import settings

from django.core.asgi import get_asgi_application
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings.settings')

application = get_asgi_application()

sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=settings.ENVIRONMENT)
asgi_app = SentryAsgiMiddleware(application)
