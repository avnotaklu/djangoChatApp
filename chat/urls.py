# chat/urls.py
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/',views.room,name='room'),
]
#urlpatterns += staticfiles_urlpatterns()
#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
