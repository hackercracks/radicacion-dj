from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('files/', include('filed.urls', namespace="files")),
    path('agents/',  include('agents.urls', namespace="agents")),

    # Api Banger Boos
    path('api/', include("filed.api.urls")),
    path('api/auth/', include("account.api.urls")),
    path('api/agent/', include("agents.api.urls")),
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)