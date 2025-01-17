import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bandmatch_project.settings')

import django
django.setup()

from datetime import datetime

from bandmatch.models import Player, Band, Advert, Message
from django.contrib.auth.models import User

#The population script

def populate():


	add_player('Jaakko1', "J", "1", 'Call me xxx', "I'm handsome", "Dumbarton Road, Glasgow", ["guitar", "drums"])

	add_player('Jaakko', "J", "K", "Call me xoxo", "I'm in a band!!", "11 Ruthven Lane, Glasgow", ["vocals"])

	add_player('Reni', "R", "2", "Bulgaria", "I'm not in a band :((", "12 Ashton Lane, Glasgow", ["piano", "bass"])

	add_player('Leif', 'Australian', 'Guy', "I wish I lived in Australia", "Men at work - Down Under ALL THE WAY!", "Glasgow :((", ["FUCKING NOTHING"])

	create_band('My chemical bromance', '7 Victoria Circus, Glasgow', 'AWESOME', 'Jaakko')

	create_band('30 Seconds to venus', '12 University Gardens, Glasgow', 'AMAZING', 'Reni')

	create_band('Blue Day', '23 Grosvenor Ln, Glasgow', 'ASTONISHING', 'Jaakko1')

	make_advert('My chemical bromance', 'deaf drummer wanted', 'no headphones for you', 'drums')

	write_message('Pick mee', "I'm the best", 'Jaakko1', ['Jaakko'])

	write_message('whatever', '', 'Jaakko', ["Jaakko1","Reni"])

	add_player('Admin', "Bandmatch", "Admin", 'IM @admin', 'Bandmatch admin')
	admin = User.objects.get_or_create(username = 'admin')[0]
	admin.set_password('admin')
	admin.save()

	add_player('test', "test", "test", '', 'test user')
	test = User.objects.get_or_create(username = 'test')[0]
	test.set_password('test')
	test.save()

	add_player('mshinoda', 'Mike', 'Shinoda', 'mikeshinoda.com',
	 "an American musician, record producer, and artist. He co-founded Linkin Park in 1996 and bands rhythm guitarist, songwriter, keyboardist, and co-vocalist.", 
	 '83 Saint Vincent Street, Glasgow', ['guitar', 'keyboard', 'vocals'])

	add_player('bdelson', 'Brad', 'Delson', 'https://twitter.com/delsononline', 
		'a musician.', '60 North Hanover Street, Glasgow', ['guitar', 'vocals'])

	add_player('jhahn', 'Joe', 'Hahn', 'https://twitter.com/joehahnlp', 
		'a turntablist and director ', '167 Renfrew St, Glasgow', ['turntables', 'sampler', 'keyboards', 'synthesizer'])

	add_player('cbennington', 'Chester', 'Bennington', 'cbennington.com',
	 'an American musician, singer, songwriter, and actor', '16 Richmond Street, Glasgow', ['vocals'])

	create_band('Linkin Perk', '84 Castle Street, Glasgow', 
		'an American rock band from Agoura Hills, California', 'cbennington', ['mshinoda', 'bdelson'])

	add_player('nsanderson', 'Neil', 'Sanderson', '',
	 'influenced by John Bonham, Danny Carey and Stewart Copeland', 'Castle Street, Glasgow', ['drums', 'vocals'])

	add_player('bstock', 'Barry', 'Stock', 'https://www.facebook.com/pages/Barry-Stock-Official/327337807289391', 
		'I use Schecter, Ibanez and PRS guitars, but prefer an Ibanez SZ320', 
		'12 Rose Street, Glasgow', ['guitar'])

	create_band('4 days grace', '7 Renfrew St, Glasgow', 
	 	'a Canadian rock band formed in Norwood, Ontario, Canada in 1992, emigrated to glasgow the year after', 'nsanderson')

	add_player('akiedis', 'Anthony', 'Kiedis', 'the yelow subarine', 'heavily influenced by bad choices', 
		'490 Sauchiehall Street, Glasgow', ['vocals'])

	add_player('csmith', 'Chad', 'Smith', '', 'musician',"500 Great Western Road, Glasgow", 
		['drums', 'percussion', 'piano', 'guitar', 'bass'])


def add_player(username, firstname, lastname, contact_info, description, location="Nowhere", instruments=[]):
	user = User.objects.get_or_create(username = username)[0]
	user.first_name = firstname
	user.last_name = lastname
	user.set_password("123")
	user.save()
	p = Player.objects.get_or_create(user = user)[0]
	p.description = description
	p.contact_info = contact_info
	for i in instruments:
		if i not in p.instruments:
			p.instruments.append(i)
	p.location = location
	p.save()


def create_band(name, location, description, founder_username, other_members=[]):
	b = Band.objects.get_or_create(name = name, location = location, description = description)[0]
	try:
		founder = Player.objects.get_or_create(user__username__exact = founder_username)[0]
		b.members.add(Player.objects.get(user__username__exact = founder.user.username))
		b.save()
	except:
		print "User with the given username doesn't exist"
	for m in other_members:
		m_profile = Player.objects.get_or_create(user__username__exact = m)[0]
		b.members.add(m_profile)
	b.save()


def write_message(title, content, sender, recipients):
	m = Message.objects.get_or_create(title = title, content = content, sender = Player.objects.get(user__username__exact = sender))[0]
	for r in recipients:
		user_recipient = Player.objects.get(user__username__exact = r)
		m.recipients.add(user_recipient)
	m.date = datetime.now()
	m.save()

def make_advert(band, title, content, looking_for):
	ad = Advert.objects.get_or_create(title = title, content = content, looking_for = looking_for,
		band = Band.objects.get(name__exact = band))[0]
	ad.save()


if __name__ == '__main__':
	print "Starting population script..."
	populate()
