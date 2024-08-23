from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),  # Spécifique au chemin 'home/'
    path('connect_as/', include('authentication.urls')),
    path('dashboard_super/', include('supervisor.urls')),
    path('dashboard_client/', include('client.urls')),
    path('authmobile/', include('authmobile.urls')),  # Spécifique au chemin 'authmobile/'
    path('client_mob/', include('client_mob.urls')),  # Spécifique au chemin 'client_mob/'
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
