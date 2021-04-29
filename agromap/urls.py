"""agromap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
#from ajax_select import urls as ajax_select_urls

#from .views import index, connexion, loggout
#from mon_ghs.views import index, connexion, loggout

admin.site.site_header = "BIENVENUS SUR AGROMAP-Traçability"
admin.site.index_title = "ADMINISTRATION AGROMAP-Traçability"

urlpatterns = [
    path('clients/', include('chocolotiers.urls')),
    #path("select2/", include("django_select2.urls")),
    path('cooperatives/', include('cooperatives.urls')),    
    # path('ajax_select/', include(ajax_select_urls)),
    path('', include('parametres.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
