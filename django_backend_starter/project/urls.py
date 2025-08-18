from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Example: include your app urls here
    # path('users/', include('users.urls')),
]
