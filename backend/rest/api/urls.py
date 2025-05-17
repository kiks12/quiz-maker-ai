from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views.uploadviewset import UploadViewSet


router = routers.DefaultRouter()
router.register(r'upload', UploadViewSet,  basename="upload")

# print("SETTINGS: ", settings.MEDIA_URL, settings.MEDIA_ROOT)
urlpatterns = [
    path("", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
