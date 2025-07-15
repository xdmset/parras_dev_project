# parras_dev_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/', include('pendientes.urls')), # Apunta a las URLs de la app pendientes
]