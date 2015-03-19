import re

from django.shortcuts import render

from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from bandmatch.models import Band, Player, Message, Advert, User, Reply
from bandmatch.forms import UserForm, PlayerForm, BandForm, AdvertForm, ReplyForm


# Create your views here.
def index(request):

    context_dict = {}

    user = request.user

    if not user.is_authenticated():
    	return HttpResponseRedirect('/bandmatch/about/')
   	
	player = Player.objects.get(user = user)
	recent_messages = player.message_set.all().order_by('date')[:5]
	context_dict['messages'] = recent_messages


    response = render(request,'bandmatch/index.html', context_dict)
    return response


def about(request):


	return render(request, 'bandmatch/about.html', {})

@login_required
def your_bands(request):
	context_dict = {}

	user = request.user

	player = Player.objects.get(user = user)

	user_bands = player.band_set.all() #should get all the bands that have that user as a member

	context_dict['bands'] = user_bands

	return render(request, 'bandmatch/your_bands.html', context_dict)

#View to display the band page.
def band(request, band_name_slug):
	context_dict = {}
	band = Band.objects.get(slug = band_name_slug)

	context_dict['name'] = band.name

	members_list = band.members.all()
	context_dict['members'] = members_list # a for loop in the html should be able to get the members

	context_dict['location'] = band.location

	context_dict['description'] = band.description

	if band.demo:
		context_dict['pic'] = band.image.url 
	else:
		context_dict['pic']= ''

	if band.demo:
		context_dict['demo'] = band.demo.url #not sure if this is how you get a file url
	else:
		context_dict['demo']= ''

	context_dict['is_member']= 0

	context_dict['slug'] = band.slug
	advert_list = Advert.objects.filter(band__exact = band)
	context_dict['adverts'] = advert_list.order_by('-date')

	if request.user.is_authenticated():
		player = Player.objects.get(user = request.user)
		if player in members_list:
			context_dict['is_member']= 1

	return render(request, 'bandmatch/band.html', context_dict)

def edit_band(request, band_name_slug):

	context_dict = {}

	context_dict['slug'] = band_name_slug

	band = Band.objects.get(slug = band_name_slug)

	context_dict['name'] = band.name

	members_list = band.members.all()
	context_dict['members'] = members_list # a for loop in the html should be able to get the members

	context_dict['location'] = band.location

	context_dict['description'] = band.description

	if band.demo:
		context_dict['pic'] = band.image.url 
	else:
		context_dict['pic']= ''

	if band.demo:
		context_dict['demo'] = band.demo.url #not sure if this is how you get a file url
	else:
		context_dict['demo']= ''

	context_dict['is_member']= 0

	if request.user.is_authenticated():
		player = Player.objects.get(user = request.user)
		if player in members_list:
			context_dict['is_member']= 1

	context_dict['slug'] = band.slug
	advert_list = Advert.objects.filter(band__exact = band)
	context_dict['adverts'] = advert_list.order_by('-date')

	context_dict['band_form'] = BandForm(instance = band)

	if request.method == 'POST':
		#Create the band and take the user to the created bands site
		band_form = BandForm(request.POST, request.FILES, instance= band)

		new_member = request.POST['suggestion']

		band.members.add(Player.objects.get(user__username = new_member))

		band.save()

		if band_form.is_valid():
			print 'valid'
			band = band_form.save(commit=False)			

			if 'image' in request.FILES:
				band.image = request.FILES['image']

			if 'demo' in request.FILES:
				band.demo = request.FILES['demo']

			band.save()

	return render(request, 'bandmatch/edit_band.html', context_dict)

def add_player(request, band_name_slug, player_username):

	band = Band.objects.get(slug = band_name_slug)

	try:
		player = Player.objects.get(user = player_username)
	except Exception, e:
		return HttpResponse('This user does not exist')
	

	band.members.add(player)
	band.save()

	return HttpResponseRedirect('/bandmatch/band/band_name_slug/edit')


#A view to create a band. Used with make_a_band.html and BandForm
@login_required
def add_band(request):

	context_dict = {}
	context_dict['created'] = False

	if request.method == 'POST':
		#Create the band and take the user to the created bands site
		band_form = BandForm(request.POST, request.FILES)
		if band_form.is_valid():
			newband = band_form.save(commit=False)
			user = request.user
			founder = Player.objects.get(user__exact = user)
			
			newband.save()

			newband.members.add(founder)

			if 'image' in request.FILES:
				newband.image = request.FILES['image']
			else:
				newband.image = settings.MEDIA_URL + 'b.png'

			if 'demo' in request.FILES:
				newband.demo = request.FILES['demo']

			newband.save()
                                

			context_dict['created'] = True
			#A redirection to the created band's site would be nice
			#Is there a more elegant way?
			url = '/bandmatch/band/' #Hardcoded! Bad :((
			url = url + newband.slug
			return HttpResponseRedirect(url)


	else:
		#Display bandform
		context_dict['band_form'] = BandForm()


	return render(request, 'bandmatch/make_a_band.html', context_dict)


#Displayes the user profile, and allows modification if its the user's own page
def profile(request, username): #could possibly use user_id here
	context_dict = {}

	user = User.objects.get(username = username)

	player = Player.objects.get(user = user)

	context_dict['username'] = username

	context_dict['first_name'] = user.first_name

	context_dict['last_name'] = user.last_name

	context_dict['description'] = player.description

	context_dict['instruments'] = player.instruments #should probably be checked how it works when instruments are a list

	user_bands = player.band_set.all()

	context_dict['bands'] = user_bands

	#we could do this or pass privacy to the html with the context_dict
	#and choose what to display there
	if player.privacy == 1: # if 1 is on and 0 is off
		context_dict['email'] = user.email #only displayed for registered users and if user allows it
		context_dict['contact_info'] = player.contact_info 
		context_dict['location'] = player.location
	else:
		context_dict['email'] = ''
		context_dict['contact_info'] =  ''
		context_dict['location'] = ''

	if player.demo:
		context_dict['demo'] = player.demo.url #not sure if this is how you get a file url
	else:
		context_dict['demo']= ''

	if player.image:
		context_dict['pic'] = player.image.url
	else:
		context_dict['pic'] = ''

	#can use this in html to display link to edit profile
	if request.user == user:
		context_dict['is_user'] = 1
	else:
		context_dict['is_user'] = 0

	return render(request, 'bandmatch/profile.html', context_dict)

#Might not be necessary.
def edit_profile(request):
	return HttpResponse("Template missing")

def register_profile(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
		user_form = UserForm(data=request.POST)
		player_form = PlayerForm(data=request.POST)

		instruments_list = player_form.data['instruments'].encode('ascii', 'ignore').lower().split(",")
		for i in range(len(instruments_list)):
			instruments_list[i] = re.sub(r"[^a-z]+", '', instruments_list[i])
		print instruments_list
		player_form.data['instruments'] = instruments_list


		# If the two forms are valid...
		if user_form.is_valid() and player_form.is_valid():
			

			# Save the user's form data to the database.
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = player_form.save(commit=False)
			profile.user = user


			#Demo? Picture?

			if 'image' in request.FILES:
				profile.image = request.FILES['image']
			elif profile.gender == 'm':
				profile.image = settings.STATIC_URL + 'images\m.jpg'
			elif profile.gender == 'f':
				profile.image = settings.STATIC_URL + 'images\pf.jpg'
			elif profile.gender == 'unknown':
				profile.image = settings.STATIC_URL + 'images\o.png'

			if 'demo' in request.FILES:
				profile.demo = request.FILES['demo']

			# Now we save the UserProfile model instance.
			profile.save()

			# Update our variable to tell the template registration was successful.
			registered = True
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect('/bandmatch/')

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print user_form.errors, player_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        player_form = PlayerForm()

    # Render the template depending on the context.
    return render(request,
            'registration/registration_form.html',
            {'user_form': user_form, 'player_form': player_form, 'registered': registered} )

def search_bands(request):
	context_dict = {}

	result_list = []

	query = request.POST['bandsquery'].lower() #maybe should include if check for request method

	#search band name
	bands_list = Band.objects.filter(name__contains = query)

	for band in bands_list:
		result_list.append(band)

	#search advert
	adverts_list = Advert.objects.filter(looking_for__contains = query)

	for ad in adverts_list:
		result_list.append(ad.band)

	#should we search description???

	context_dict['results'] = result_list

	return render(request, 'bandmatch/search_bands.html', context_dict)

def search_players(request):
	context_dict = {}

	result_list = []

	query = request.POST['playersquery']

	#search name

	players_list = Player.objects.filter(user__username__contains = query)

	for player in players_list:
		result_list.append(player)

	players_list = Player.objects.filter(user__first_name__contains = query)

	for player in players_list:
		result_list.append(player)

	players_list = Player.objects.filter(user__last_name__contains = query)

	for player in players_list:
		result_list.append(player)

	#search instruments
	players_list_instr = Player.objects.all()

	for player in players_list_instr:
		if query in player.instruments:
			result_list.append(player)

	#description???

	context_dict['results'] = result_list

	return render(request, 'bandmatch/search_players.html', context_dict)

def advanced_search(request):
	return render(request, 'bandmatch/advanced_search.html', {})

@login_required
def user_logout(request):
    #Since we know the user is logged in, we can now just log them out.
   logout(request)

    #Take the user back to the homepage.
   return HttpResponseRedirect('/bandmatch/')


#A view for posting an advert
#Maybe take in the band-name-slug as an argument, and map this ad to that band using the slug.
def post_advert(request, band_name_slug):

	if request.method == 'POST':
		#Make the advert, post it, and direct user somewhere
		advert_form = AdvertForm(request.POST)
		advert = advert_form.save(commit=False)

		advert.band = Band.objects.get(slug = band_name_slug)

		advert.save()

		return HttpResponseRedirect(reverse('band', args=[band_name_slug])) #Return the user back to the bandpage.




	else:
		advert_form = AdvertForm()

		return render(request, 'bandmatch/post_advert.html', {'advert_form' : advert_form, 'band_name_slug' : band_name_slug})

#A view to display an advert. Accessible from band site. Will display the adverts contents, and it's replies.
def display_advert(request, band_name_slug, advert):
	context_dict = {}

	advertobject = Advert.objects.get(id = advert)
	context_dict['content'] = advertobject.content
	context_dict['band_name_slug'] = band_name_slug
	context_dict['advert'] = advert

	if request.method == 'POST':
		#A reply was posted - create it
		reply_form = ReplyForm(request.POST)
		newreply = reply_form.save(commit = False)

		newreply.advert = advertobject

		user = request.user
		replier = Player.objects.get(user = user)
		newreply.replier = replier
		newreply.save()

	#Get the replyform
	context_dict['reply_form'] = ReplyForm()

	#Get all the replies of the advert
	reply_list = Reply.objects.filter(advert = advertobject)
	context_dict['reply_list'] = reply_list
	print reply_list

	return render(request, 'bandmatch/display_advert.html', context_dict)




def get_usernames_list(max_results=10, starts_with=''):
	userlist = []
	if starts_with:
		if max_results > 0:
			user_list = Player.objects.filter(user__username__istartswith = starts_with)[:max_results]
		else:
			user_list = Player.objects.filter(user__username__istartswith = starts_with)

	return user_list


def suggest_username(request):
        user_list = []
        starts_with = ''
        if request.method == 'GET':
                starts_with = request.GET['suggestion']

        if starts_with != '':
        	user_list = get_usernames_list(10, starts_with)

        print user_list

        return render(request, 'bandmatch/user_list.html', {'user_list': user_list })

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
   if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
       username = request.POST['username']
       password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
       user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
       if user:
            # Is the account active? It could have been disabled.
           if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
               login(request, user)
               return HttpResponseRedirect('/bandmatch/')
           else:
                # An inactive account was used - no logging in!
               return HttpResponse("Your bandmatch account is disabled.")
       else:
            # Bad login details were provided. So we can't log the user in.
           print "Invalid login details: {0}, {1}".format(username, password)
           return HttpResponse("Wrong username/password combination.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
   else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
       return render(request, 'bandmatch/login.html', {})


