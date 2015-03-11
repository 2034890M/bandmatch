from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin






class Player(models.Model):
	user = models.OneToOneField(User)

#	name = models.CharField(max_length = 128) 	#Forename/surname or just name?
#	email = models.EmailField(max_length = 254)
	contact_info = models.TextField()
	description = models.TextField()
	#Preferences can be included in your own description?
	privacy = models.IntegerField(default=1)
	demo = models.FileField(upload_to = 'player_demos', blank = True) #How to have multiple (from 0 to n) demos? 
	instrument = models.CharField(max_length = 128, default = 'None') #Need to have this as a list of strings
	location = models.CharField(max_length = 256, default = 'Nowhere')
	image = models.ImageField(upload_to ='profile_images', blank = True)
	
	def __unicode__(self):
		return self.user.username
	





class Message(models.Model):
	title = models.CharField(max_length = 128) #May need to be changed
	content = models.TextField()
	sender = models.ForeignKey('Player', related_name='sender')
#	The relationship is yet to be defined, so need to use the name, not the object
#	---> Use 'Player' rather than Player
#	See https://docs.djangoproject.com/en/1.7/ref/models/fields/#lazy-relationships
	recipients = models.ManyToManyField('Player') 
	date = models.DateField(auto_now_add=True)

	def __unicode__(self):
		return self.title + ': ' + self.content


#Possible to gather "when a member joined the band" - data easily.
# See https://docs.djangoproject.com/en/1.7/ref/models/fields/#django.db.models.ManyToManyField.through

class Band(models.Model):
	#Genres as a separate field for easier queries?
	name = models.CharField(max_length = 128)
	demo = models.FileField(upload_to = 'band_demos', blank = True)
	location = models.CharField(max_length = 256)
	description = models.TextField()
	image = models.ImageField(upload_to = 'band_images', blank = True)
	members = models.ManyToManyField('Player')

	def __unicode__(self):
		return self.name



class Advert(models.Model):

#	What need to happen is:
#	When a band gets deleted - all it's adverts are deleted also!

	band = models.ForeignKey(Band) #Cascade deletion?
	title = models.CharField(max_length = 128)
	content = models.TextField()
	date = models.DateField(auto_now_add=True) #date is set when the object is created, cannot be edited
	looking_for = models.CharField(max_length = 256) #Need to have this as a list??

	def __unicode__(self):
		return self.title


admin.site.register(Advert)
admin.site.register(Message)
