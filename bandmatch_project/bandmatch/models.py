from django.db import models

# Create your models here.


#Player

class Player(models.Model):
	name = models.CharField(max_length = 128) 	#Forename/surname or just name?
	email = models.EmailField(max_length=254)
	contact_info = models.TextField()
	description = models.TextField()
	#Preferences can be included in your own description?
	privacy = models.IntegerField(default=1)
	demo = models.FileField(upload_to = 'demos', blank = True) #How to have multiple (from 0 to n) demos? 
	





#Message


#Band


#Advert