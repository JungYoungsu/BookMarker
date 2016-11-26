"""bm_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from main import views as main_views

urlpatterns = [
	url(r'^book/', include('book.urls')),
	url(r'^location/', include('location.urls')),
	
	url(r'^$', main_views.index),
	url(r'^shelfs/', main_views.shelfs),
	url(r'^books/', main_views.books),	
	url(r'^addbooks/', main_views.addbooks),
	url(r'^comments/', main_views.comments),
	url(r'^addcomment/', main_views.addcomment),
	
    url(r'^admin/', admin.site.urls),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
