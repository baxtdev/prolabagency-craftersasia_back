"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include

admin.site.site_title = "Администрирование сайта Crafters Asia"
admin.site.site_header = "Crafters Asia Admin"
admin.site.index_title = "Администрирование сайта Crafters Asia"

from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from api.endpoints import urlpatterns as api_urls

from apps.store.views import create_item
from apps.chat.views import start_chat,rooms
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('rest_framework.urls')), 
    path('api/v1/', include(api_urls)),
    path('', RedirectView.as_view(url='/api/v1/swagger/')),
    path('create-item/',create_item),
    path('chat/<uuid>', start_chat, name='start_chat'),
    path("rooms/", rooms, name="rooms")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)