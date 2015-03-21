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

	make_advert('My chemical bromance', 'deaf drummer wanted', 'no headphones for you', 'drums')

	write_message('Pick mee', "I'm the best", 'Jaakko1', ['Jaakko'])

	write_message('whatever', '', 'Jaakko', ["Jaakko1","Reni"])

	add_player('Admin', 'IM @admin', 'Bandmatch admin')
	admin = User.objects.get_or_create(username = 'admin')[0]
	admin.set_password('admin')
	admin.save()






def add_player(username, contact_info, description):
	user = User.objects.get_or_create(username = username)[0]
	user.set_password("123")
	user.save()
	p = Player.objects.get_or_create(user = user)[0]
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


def write_message(title, content, sender, recipients):
	m = Message.objects.get_or_create(title = title, content = content, sender = Player.objects.get(user__username__exact = sender))[0]
	for r in recipients:
		user_recipient = Player.objects.get(user__username__exact = r)
		m.recipients.add(user_recipient)
	m.save()

def make_advert(band, title, content, looking_for):
	ad = Advert.objects.get_or_create(title = title, content = content, looking_for = looking_for,
	 band = Band.objects.get(name__exact = band))[0]
	ad.save()




if __name__ == '__main__':
	print "Starting population script..."
	populate()