from django.conf.urls import url
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # ex: /
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

