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

		b1 = create_band("The awesomenauts", "Glasgow", "The best of the best", "Jaakko", ["Alex", "Carly", "Leif"])
		b2 = create_band("My solo career", "Glasgow", "Just me singing", "Reni")

		create_message("YOU ALL FAILED", "NONE SHALL PASS", "Leif", ["Alex", "Carly", "Reni"])
		create_message("Full marks", "Aweomse job. You aced it all!", "Leif", ["Jaakko"])

		a1 = create_advert(b1, "In need of a rockstar", "None of us can really play", "guitar")

		r1 = create_reply(a1, l, "I can play")
	#What and how to test?

	def test_index_notloggedin_redirects_to_about(self):

		
		#Not logged in users accessing the index page should be redirected to the about page.
	

		response_index = self.client.get(reverse('index'))
		#A user who hasn't logged in shouldn't have any response.content
		self.assertEqual(response_index.content, '')

		self.assertRedirects(response_index, reverse('about'))

	def test_index_loggedin_does_not_redirect(self):



		testClient = create_player("test", "Use me for client login in tests", "Capiche?", "", "Testland")

		login = self.client.login(username="test", password="123")

		self.assertEqual(login, True)

		response_index = self.client.get(reverse('index'))

		self.assertEqual(response_index.status_code, 200)


	def test_your_bands(self):
		
		#The template should contain a list of your bands.
		

		#login as jaakko
		login = self.client.login(username="Jaakko", password="123")
		self.assertTrue(login)

		#Get the band list. The name should be in the template.
		response_your_bands = self.client.get(reverse('your_bands'))
		self.assertIn("The awesomenauts", response_your_bands.content)


		#Send a message to yourself, and see that it's displayed correctly.
	def test_send_message(self):

		login = self.client.login(username="Jaakko", password="123")
		self.assertTrue(login)	

		#Index page shouldn't have any mention of "TEST MESSAGE"
		response_index = self.client.get(reverse('index'))
		self.assertNotIn("TEST MESSAGE", response_index.content)

		#Send a message to yourself
		self.client.post(reverse('send_message'), {'suggestion':"Jaakko", 'title':"title", 'content': 'TEST MESSAGE'})
		response_index = self.client.get(reverse('index'))

		#Message should be displayed on index page.
		self.assertIn("TEST MESSAGE", response_index.content)


	def test_index_displays_only_most_recent_messages(self):
		#login
		login = self.client.login(username="Jaakko", password="123")
		self.assertTrue(login)

		#Send yourself a message and see that it's displayed on index page
		self.client.post(reverse('send_message'), {'suggestion':"Jaakko", 'title':"title", 'content': 'TEST MESSAGE'})
		response_index = self.client.get(reverse('index'))
		self.assertIn("TEST MESSAGE", response_index.content)

		#Index page should display the 4 most recent messages. Fill the page with spam
		self.client.post(reverse('send_message'), {'suggestion':"Jaakko", 'title':"title", 'content': 'SPAM'})
		self.client.post(reverse('send_message'), {'suggestion':"Jaakko", 'title':"title", 'content': 'SPAM'})
		self.client.post(reverse('send_message'), {'suggestion':"Jaakko", 'title':"title", 'content': 'SPAM'})
		self.client.post(reverse('send_message'), {'suggestion':"Jaakko", 'title':"title", 'content': 'SPAM'})

		#The original message should not be displayed on the index page anymore
		response_index = self.client.get(reverse('index'))
		self.assertNotIn("TEST MESSAGE", response_index.content)

       

        def test_Profile_updating(self):

##                #login
                login = self.client.login(username="Jaakko", password="123")
		self.assertTrue(login)                
                
                #check previous details
		response_Address = self.client.get(reverse('profile', args=["Jaakko"]))
                self.assertIn("Winton Drive 24, Glasgow", response_Address.content)
                self.assertIn("I used to play guitar", response_Address.content)                
                self.assertIn("guitar", response_Address.content)
                
##              #change address
                create_player("Jaakko","The cake is a lie!","Aperture loboratories",["HandHeld quantum tunneling device"],"Winton Drive, Glasgow")
	
                #check that the address, instrument and info have changed
                response_Address = self.client.get(reverse('profile', args=["Jaakko"]))
                self.assertIn("Winton Drive, Glasgow", response_Address.content)
                self.assertIn("The cake is a lie!", response_Address.content)
                
                self.assertIn("HandHeld quantum tunneling device", response_Address.content)

        def test_automated_mssage_when_added_to_band(self):

		login = self.client.login(username="Jaakko", password="123")
		self.assertTrue(login)

		create_band("J", "Glasgow", "The best of the best", "Jaakko", "")

                response_Address = self.client.get(reverse('index'))
                self.assertIn("J", response_Address.content)
		
                
           
                
####Create methods below.


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




#Helper methods for the models ? Might be unecessary, as they'd most likely be "get" methods, which are 1 line of in themselves anyway.



if __name__ =='__main__':
	ModelTestCase()
