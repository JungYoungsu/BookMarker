from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^getbook/', views.getBook, name='getbook'),
	url(r'^readxls/', views.readXLS, name='readxls'),
]