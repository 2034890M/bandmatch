import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bandmatch_project.settings')

import django
django.setup()

from bandmatch.models import Player, Band, Advert, Message
from django.contrib.auth.models import User


#The population script




def populate():
	add_player('Jaakko1', 'Call me xxx', "I'm handsome")

	add_player('Jaakko', "Call me xoxo", "I'm in a band!!")

	add_player('Reni', "Bulgaria", "I'm not in a band :((")

	create_band('My chemical bromance', 'Glasgow', 'AWESOME', 'Jaakko')












def add_player(username, contact_info, description):
	user = User.objects.get_or_create(username__exact = username)[0]
	p = Player.objects.get_or_create(user__exact = user)[0]
	p.description = description
	p.contact_info = contact_info
	p.save()


def create_band(name, location, description, founder_username):
	b = Band.objects.get_or_create(name = name, location = location, description = description)[0]
	try:
		founder = Player.objects.get_or_create(user__username__exact = founder_username)[0]
		b.members.add(Player.objects.get(user__username__exact = founder.user.username))
		b.save()
	except:
		print "User with the given username doesn't exist"
	print b.members.all()





if __name__ == '__main__':
	print "Starting population script..."
	populate()