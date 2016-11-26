from __future__ import unicode_literals

from django.db import models

# Create your models here.
class APinfo(models.Model):
	mac = models.CharField(max_length=16, default=None) 
	num = models.IntegerField()

class Location(models.Model):
	num = models.IntegerField()
	top = models.IntegerField()
	left = models.IntegerField()

class APLO(models.Model):
	ap = models.ForeignKey('APinfo', null=True)
	lo = models.ForeignKey('Location', null=True)

class Seat(models.Model):
	num = models.IntegerField()
	seatgroup = models.ForeignKey('SeatGroup', null=True)

class SeatGroup(models.Model):
	num = models.IntegerField()
	location = models.ForeignKey('Location', null=True)
	location2 = models.IntegerField(default=0)
	top = models.IntegerField(default=0, null=True)
	left = models.IntegerField(default=0, null=True)