"""mysite URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from core.api.views import ConfirmEmailView

routes = getattr(settings, 'REACT_ROUTES', [])

urlpatterns = [
    url(r'^(%s)?$' % '|'.join(routes), TemplateView.as_view(template_name='react.html')),
    path('admin/', admin.site.urls),  
    # path('', TemplateView.as_view(template_name='react.html')),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api-auth/', include('rest_framework.urls')),
    # path('accounts/password/reset/key/<slug>/', capture_url, name='password_reset_confirm_custom'),
    path('accounts/', include('allauth.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/account-confirm-email/<key>/', ConfirmEmailView.as_view(),name="custom-email-confirm-api"),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('api/', include('core.api.urls',namespace='core-api')),
]
   

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
