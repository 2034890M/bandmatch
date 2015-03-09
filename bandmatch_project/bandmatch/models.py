from django.db import models
from django.contrib.auth.models import User



# Create your models here.


#Player

class Player(models.Model):
	user = models.OneToOneField(User)

#	name = models.CharField(max_length = 128) 	#Forename/surname or just name?
#	email = models.EmailField(max_length = 254)
	contact_info = models.TextField()
	description = models.TextField()
	#Preferences can be included in your own description?
	privacy = models.IntegerField(default=1)
	demo = models.FileField(upload_to = 'player_demos', blank = True) #How to have multiple (from 0 to n) demos? 
	instrument = models.CharField(max_length = 128) #Need to have this as a list of strings
	location = models.CharField(max_length = 256)
	image = models.ImageField(upload_to 'profile_images')
	





#Message
class Message(models.Model):
	title = models.CharField(max_length = 128) #May need to be changed
	content = models.TextField()
	sender = models.ForeignKey(Player)
	recipients = models.ManyToManyField(Player)
	date = models.DateField()


#Band
class Band(models.Model):
	#Genres as a separate field for easier queries?
	demo = models.FileField(upload_to = 'band_demos', blank = True)
	location = models.CharField(max_length = 256)
	description = models.TextField()
	image = models.ImageField(upload_to = 'band_images')
	members = models.ManyToManyField(Player)

#Advert

class Advert(models.Model):

#	What need to happen is:
#	When a band gets deleted - all it's adverts are deleted also!

	band = models.ForeignKey(Band) #Cascade deletion?
	title = models.CharField(max_length = 128)
	content = models.TextField()
	date = models.DateField()
	looking_for = models.CharField(max_length = 256) #Need to have this as a list??