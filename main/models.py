from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Book_SearchDate(models.Model):
	date = models.DateField()
	count = models.IntegerField()
	
class Book_AddDate(models.Model):
	date = models.DateField()
	count = models.IntegerField()
	
class Comments(models.Model):
	content = models.TextField()
	time = models.DateTimeField(auto_now=False, auto_now_add=False)