from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('livres.api_urls')),  # ← API REST
    path('', include('livres.urls')),          # ← Vos URLs existantes
]