from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('acesso/', include('usuarios.urls')),
    path('plataforma/', include('plataforma.urls')),
    path("", lambda request: redirect('/acesso/login')),   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
