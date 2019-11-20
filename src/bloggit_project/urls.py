"""bloggit_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view
from rest_auth.views import PasswordResetConfirmView

from bloggit_project.utils.views import CustomPasswordResetView, CustomRegisterView
schema_view = get_swagger_view(title='bloggit API')

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/register/', CustomRegisterView.as_view(), name='error'),
    path('api/v1/api-docs', schema_view),
    path('api/v1/posts/', include('posts_app.urls')),
    path('api/v1/users/', include('users_app.urls')),
    path('api/v1/password-reset/', CustomPasswordResetView.as_view(), name="password_reset"),
    re_path(r'^api/v1/password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
