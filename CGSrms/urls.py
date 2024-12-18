"""
URL configuration for CGSrms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path,include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.http import HttpResponseNotFound


def custom_404(request, *args, **kwargs):
    return HttpResponseNotFound("The page you are looking for does not exist.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/accounts/home_login/', permanent=False)),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace = 'accounts')),  # URLs related to user accounts
    path('CGS_Records/', include(('CGS_Records.urls', 'CGS_Records'), namespace='CGS_Records')),
    path('CGS_Dashboard/', include(('CGS_Dashboard.urls', 'CGS_Dashboard'), namespace='CGS_Dashboard')),
    path('admin/PhD_Doctor_of_Management_Evaluation_of_Grades/', custom_404),
    
]  

if settings.DEBUG:  # Ensure these are only added in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

