"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.contrib.auth.urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from crm import api_urls
from .views import health
from .views import trigger_error
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
                  path('i18n/', include('django.conf.urls.i18n')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += i18n_patterns(
    path('sentry-debug/', trigger_error),
    path('health/', health, name='health'),
    path('admin/', admin.site.urls),
    path('properties/', include('properties.urls')),
    path('', include(('ui.urls', 'ui'), namespace='ui')),
    path('api/', include(api_urls)),
)
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = 'crm.views.bad_request'
handler403 = 'crm.views.permission_denied'
handler404 = 'crm.views.page_not_found'
handler500 = 'crm.views.server_error'
