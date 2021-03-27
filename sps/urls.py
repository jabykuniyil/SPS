
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student.url')),
    path('coordinator/', include('coordinator.url')),
    path('spsadmin/', include('spsadmin.url')),
    path('oauth/', include('social_django.urls', namespace='social')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
