# -*- coding: utf-8 -*-

from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.utils.encoding import iri_to_uri
from django.views.static import serve as staticserve

urlpatterns = [
    url(r'', include('base.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^account/', include('edoprofile.urls')),
    url(r'^editor/', include('editor.urls')),
    url(r'^history/', include('dochistory.urls')),
]

if settings.DEBUG:
    media_url = settings.MEDIA_URL[1:] if settings.MEDIA_URL.startswith('/') \
        else settings.MEDIA_URL

    urlpatterns += (
        url(r'^{0}(?P<path>.*)$'.format(iri_to_uri(media_url)),
         staticserve, {'document_root': settings.MEDIA_ROOT}
         ),
    )

urlpatterns.extend(i18n_patterns(prefix_default_language=True))
