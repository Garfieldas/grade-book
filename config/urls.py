from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('home/', include('dashboard.urls')),
    path('academics/', include('academics.urls')),
    path('grades/', include('grades.urls')),
]
