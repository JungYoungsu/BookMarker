from __future__ import unicode_literals

from django.db import models

# Create your models here.

def UploadImage(instance, filename):
	return filename

class Bookshelf(models.Model):
	name = models.CharField(max_length=64, default=None) 
	lower_mark = models.CharField(max_length=128) 
	upper_mark = models.CharField(max_length=128) 

class Book(models.Model):
	cid = models.IntegerField() #Contents number
	type = models.CharField(max_length=128) 
	title = models.CharField(max_length=128) 
	author = models.CharField(max_length=128)
	mark = models.CharField(max_length=128) 
	sideImage = models.ImageField(upload_to = 'booksideimage', null=True, default=None)
	
	def __unicode__(self):
		return self.name
	
	bookshelf = models.ForeignKey('Bookshelf', null=True)
	


	
	