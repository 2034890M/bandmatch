import ast
from datetime import datetime

from django.db import models


from django.test import TestCase
from django.core.urlresolvers import reverse

from bandmatch.models import Player, Band, Message, Advert, Reply, ListField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify





# Create your tests here.


#Would need a fixture = setup and teardown

#Helper methods:
#Creation methods for all the models
#Edit methods for Player + band to check that the changing of details works correctly



#A TestCase for models and editing them.
class ModelTestCase(TestCase):
	#No need for setUp as we're only testing the list field = Very few and very detailed objects



	#The only relevant thing to test is ListField, as it is self-coded.


	def test_player_no_intruments_emtpy_list(self):
		no_instruments = create_player("No", "Instruments", "I can't play lol", "", "Rock city")
		self.assertEqual(no_instruments.instruments, [])


	def test_player_one_instrument(self):
		one_instrument = create_player("Just", "One", "Instrument I can play", ["violin"], "Violin town")
		self.assertEqual(one_instrument.instruments, ["violin"])


	def test_player_multiple_instruments(self):
		many_instruments = create_player("Awmagad", "So many", "Instruments I can play", ["guitar", "violin", "piano", "drums"], "Music land")
		self.assertNotEqual(many_instruments.instruments, ["violin", "piano", "drums"])

	#What else to test from the ListField?


	#tearDown not needed, way to go Django testcases!


class ViewTestSuite(TestCase):

	def setUp(self):
		j = create_player("Jaakko", "I used to play guitar", "M, 22, call for hot action", ["guitar"], "Winton Drive 24, Glasgow")
		a = create_player("Alex", "I'm super drummer. Nearly as cool as Jaakko", "I live in Glasgo Uni Campus, or do I?", ["drums"], "Nowhere")
		c = create_player("Carly", "Wee scottish", "Glasgow Uni xxx", ["bagpipes"], "Glasgow")
		r = create_player("Reni", "Hi", "My irc is Hax0r", [], "Sofia")
		l = create_player("Leif", "Australian, kangaroo loving guy", "Please print this form, sign it, scan it and send it to my email. And yes, we're studying computing science.", ["Nothing"], "Moolooloo, Australia")
		testClient = create_player("test", "Use me for client login in tests", "Capiche?", "", "Testland")

		b1 = create_band("The awesomenauts", "Glasgow", "The best of the best", "Jaakko", ["Alex", "Carly", "Leif"])
		b2 = create_band("My solo career", "Glasgow", "Just me singing", "Reni")

		create_message("YOU ALL FAILED", "NONE SHALL PASS", "Leif", ["Alex", "Carly", "Reni"])
		create_message("Full marks", "Aweomse job. You aced it all!", "Leif", ["Jaakko"])

		a1 = create_advert(b1, "In need of a rockstar", "None of us can really play", "guitar")

		r1 = create_reply(a1, l, "I can play")
	#What and how to test?

	def test_index_notloggedin_redirects_to_about(self):

		"""
		Not logged in users accessing the index page should be redirected to the about page.
		"""
		response = self.client.get(reverse('index'))
		self.assertRedirects(response, reverse('about'), status_code=302, target_status_code=200, msg_prefix='')


	def test_index_loggedin_delivers_data(self):

		"""
		Logged in users shouldn't be redirected from the index page. 
		"""


		tc = self.client.login(user="test", password="123")
		self.assertTrue(tc.logged_in)
		response = self.client.get(reverse('index'))
		self.assertRedirects(response, reverse('about'), status_code=302, target_status_code=200, msg_prefix='')








"""
Create methods below.

"""
def create_player(username, description, contact_info, instruments, location):
	user = User.objects.get_or_create(username = username)[0]
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
	return p


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
	return b

def create_message(title, content, sender, recipients):
	m = Message.objects.get_or_create(title = title, content = content, sender = Player.objects.get(user__username__exact = sender))[0]
	for r in recipients:
		user_recipient = Player.objects.get(user__username__exact = r)
		m.recipients.add(user_recipient)
	m.date = datetime.now()
	m.save()
	return m

def create_advert(band, title, content, looking_for):
	ad = Advert.objects.get_or_create(title = title, content = content, looking_for = looking_for,
		band = band)[0]
	ad.save()
	return ad

def create_reply(advert, replier, content):
	repl = Reply.objects.get_or_create(advert=advert, replier=replier, content=content)[0]
	repl.save()
	return repl



"""
Helper methods for the models ? Might be unecessary, as they'd most likely be "get" methods, which are 1 line of in themselves anyway.
"""


if __name__ =='__main__':
	ModelTestCase()