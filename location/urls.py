from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^map/', views.showmap, name='showmap'),
	url(r'^path/', views.path, name='path'),
	url(r'^setlocation/', views.setlocation, name='setlocation'),
	url(r'^setseat/', views.setseat, name='setseat'),
	url(r'^setshelf/', views.setshelf, name='setshelf'),
]