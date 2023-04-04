from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app.urls')),
    #------------------- For every Project
    path('api/', include('app.api.urls'))
    #------------------- For every Project
]

# connecting media URL to media ROOT
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)