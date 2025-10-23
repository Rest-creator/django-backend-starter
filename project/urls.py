"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView
    )

API_VERSION = "api/v1"

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth URLs for browsable API
    path('api-auth/', include('rest_framework.urls')),

    # loan application module endpoint entry
    path(f"{API_VERSION}/loan-application/", include("core.loan_application_module.implementation.urls")),

    # URLs for 
    path(f'{API_VERSION}/schema', SpectacularAPIView.as_view(), name='schema'),
    path(f'{API_VERSION}/schema/redoc', SpectacularRedocView.as_view(url_name="schema"), name='redoc'),
    path(f'{API_VERSION}/schema/swagger-ui', SpectacularSwaggerView.as_view(url_name="schema"), name='swagger-ui'),
]
