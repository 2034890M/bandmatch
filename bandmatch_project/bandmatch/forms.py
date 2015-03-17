from django import forms
from bandmatch.models import Player, Band
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password')

class PlayerForm(forms.ModelForm):

	contact_info = forms.CharField(widget=forms.Textarea) #http://stackoverflow.com/questions/7302889/textfield-missing-in-django-forms
	description = forms.CharField(widget=forms.Textarea)
	#Add privacy!
	demo = forms.FileField(required = False)
	instruments = forms.CharField(max_length = 128, initial = 'None')
	location = forms.CharField(max_length = 256, initial = 'Nowhere')
	image = forms.ImageField(required = False)

	class Meta:
		model = Player
		exclude = ('location', 'privacy', 'user')

#A form to create a band. Adding a player will need to be done after a creating a band.
class BandForm(forms.ModelForm):

	name = forms.CharField(max_length = 128)

	location = forms.CharField(max_length = 256, initial = 'Nowhere')
	description = forms.CharField(widget=forms.Textarea)


	demo = forms.FileField(required = False)
	image = forms.ImageField(required = False)

	class Meta:
		model = Band
		exclude = ('slug', 'members')