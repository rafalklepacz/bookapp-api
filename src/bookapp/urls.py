"""bookapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from pydoc import describe
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="BookApp API",
        default_version='v1',
        description="Aby się zalogować do **SwaggerUI**, należy wywołać metodę `auth\` z odpowiednimi wartościami `username` i `password`, a następnie kliknąć przycisk `Authorize` i wygenerowany token wkleić w pole tekstowe z prefiksem 'Bearer ', czyli `Bearer {token}`."
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    re_path(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    re_path(r'$', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc')
]
