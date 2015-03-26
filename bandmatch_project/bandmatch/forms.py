from django import forms
from bandmatch.models import Player, Band, Advert, Message, Reply
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

class PlayerForm(forms.ModelForm):

	gender = forms.ChoiceField(choices = (('unknown', 'do not wish to specify'), ('m', 'male'),('f', 'female')))
	privacy = forms.ChoiceField(choices = ((1, 'on'),(0, 'off')))
	contact_info = forms.CharField(widget=forms.Textarea) #http://stackoverflow.com/questions/7302889/textfield-missing-in-django-forms
	description = forms.CharField(widget=forms.Textarea)
	#Add privacy!
	demo = forms.FileField(required = False)
	instruments = forms.CharField(max_length = 128, initial = 'None', required = False)
	location = forms.CharField(max_length = 256, initial = 'Nowhere')
	image = forms.ImageField(required = False)

	class Meta:
		model = Player
		exclude = ('location', 'privacy', 'user')

#A form to create a band. Adding a player will need to be done after a creating a band.
class BandForm(forms.ModelForm):

	name = forms.CharField(max_length = 128, help_text = 'Name')

	location = forms.CharField(max_length = 256, initial = 'Nowhere', help_text = 'Location')
	description = forms.CharField(widget=forms.Textarea, help_text = 'Description')


	demo = forms.FileField(required = False, help_text = 'Demo')
	image = forms.ImageField(required = False, help_text = 'Image')

	class Meta:
		model = Band
		exclude = ('slug', 'members')

#Work in progress
class MessageForm(forms.ModelForm):

	title = forms.CharField(max_length = 128)

	content = forms.CharField(widget = forms.Textarea)
	#How to add recipients?
	#A message for a player vs a message for an advert??
	class Meta:
		model = Message
		fields = ('title', 'content',)

class AdvertForm(forms.ModelForm):

	title = forms.CharField(max_length = 128)
	content = forms.CharField(widget = forms.Textarea)
	looking_for = forms.CharField(max_length = 256) #Might need this as an ticked input or scrolldown box

	class Meta:
		model = Advert
		exclude = ('band', 'date')

class ReplyForm(forms.ModelForm):

	content = forms.CharField(widget = forms.Textarea)

	class Meta:
		model = Reply
		fields = ('content', )

