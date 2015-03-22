import re

from django.shortcuts import render

from django.conf import settings

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from bandmatch.models import Band, Player, Message, Advert, User, Reply
from bandmatch.forms import UserForm, PlayerForm, BandForm, AdvertForm, ReplyForm, MessageForm


# Create your views here.
def index(request):

    context_dict = {}

    user = request.user

    if not user.is_authenticated():
    	return HttpResponseRedirect('/bandmatch/about/')
   	
    player = Player.objects.get(user = user)
    recent_messages = player.message_set.all().order_by('date')[:5]
    context_dict['messages'] = recent_messages

    player_address = player.location
    players = []
    players2 = []
    #this should look through all the players and add their details to the dictionary
    users = Player.objects.all()
    for each in users:
        if each.user == user:
            continue        #emphasis on should
        info = []
        
        info.append(each.user)
        info.append(each.contact_info)
        players.append(info)
        players2.append((each.location))
    bandAdds = []
    bandData = []
    bands = Band.objects.all()
    for each in bands:
        info = []
        info.append(each.name)
        info.append(each.description)     
        #info.append(members)
        bandAdds.append(each.location)
        bandData.append(info)
        
    context_dict['address']=player_address
    context_dict['addresses']=players2
    context_dict['players']=players
    context_dict['bandAdds']=bandAdds
    context_dict['bandData']=bandData
    
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

def get_bandDetails(band_name_slug):
	context_dict = {}

	band = Band.objects.get(slug = band_name_slug)

	context_dict['slug'] = band_name_slug

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

	return context_dict

#View to display the band page.
def band(request, band_name_slug):
	context_dict = {}
	band = Band.objects.get(slug = band_name_slug)

	# context_dict['slug'] = band_name_slug

	# context_dict['name'] = band.name

	# members_list = band.members.all()
	# context_dict['members'] = members_list # a for loop in the html should be able to get the members

	# context_dict['location'] = band.location

	# context_dict['description'] = band.description

	# if band.image:
	# 	context_dict['pic'] = band.image.url 
	# else:
	# 	context_dict['pic']= ''

	# if band.demo:
	# 	context_dict['demo'] = band.demo.url #not sure if this is how you get a file url
	# else:
	# 	context_dict['demo']= ''

	members_list = band.members.all()

	context_dict = get_bandDetails(band_name_slug)

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

	band = Band.objects.get(slug = band_name_slug)

	# context_dict['slug'] = band_name_slug

	# context_dict['name'] = band.name

	# members_list = band.members.all()
	# context_dict['members'] = members_list # a for loop in the html should be able to get the members

	# context_dict['location'] = band.location

	# context_dict['description'] = band.description

	# if band.demo:
	# 	context_dict['pic'] = band.image.url 
	# else:
	# 	context_dict['pic']= ''

	# if band.demo:
	# 	context_dict['demo'] = band.demo.url #not sure if this is how you get a file url
	# else:
	# 	context_dict['demo']= ''

	context_dict = get_bandDetails(band_name_slug)

	context_dict['is_member']= 0

	if request.user.is_authenticated():
		player = Player.objects.get(user = request.user)
		if player in members_list:
			context_dict['is_member']= 1

	advert_list = Advert.objects.filter(band__exact = band)
	context_dict['adverts'] = advert_list.order_by('-date')

	context_dict['band_form'] = BandForm(instance = band)

	if request.method == 'POST':
		#Create the band and take the user to the created bands site
		band_form = BandForm(request.POST, request.FILES, instance= band)

		if request.POST.__contains__('suggestion'):
			new_member = request.POST['suggestion']
			band.members.add(Player.objects.get(user__username = new_member))#try/except?
			band.save()

		if request.POST.__contains__('suggest_mem'):
			removed_member = request.POST['suggest_mem']
			band.members.remove(Player.objects.get(user__username = removed_member))
			band.save()

		members_list = band.members.all()
		context_dict['members'] = members_list

		if band_form.is_valid():
			band = band_form.save(commit=False)			

			if 'image' in request.FILES:
				band.image = request.FILES['image']

			if 'demo' in request.FILES:
				band.demo = request.FILES['demo']

			band.save()

			band_name_slug = band.slug

			# context_dict['slug'] = band_name_slug

			# context_dict['name'] = band.name

			# context_dict['location'] = band.location

			# context_dict['description'] = band.description

			# if band.demo:
			# 	context_dict['pic'] = band.image.url 
			# else:
			# 	context_dict['pic']= ''

			# if band.demo:
			# 	context_dict['demo'] = band.demo.url #not sure if this is how you get a file url
			# else:
			# 	context_dict['demo']= ''

			context_dict.update(get_bandDetails(band_name_slug))

	return render(request, 'bandmatch/edit_band.html', context_dict)

# def add_player(request, band_name_slug, player_username):

# 	band = Band.objects.get(slug = band_name_slug)

# 	try:
# 		player = Player.objects.get(user = player_username)
# 	except Exception, e:
# 		return HttpResponse('This user does not exist')
	

# 	band.members.add(player)
# 	band.save()

# 	return HttpResponseRedirect('/bandmatch/band/band_name_slug/edit')

# def remove_player(request, band_name_slug, player_username):

# 	band = Band.objects.get(slug = band_name_slug)

# 	try:
# 		player = Player.objects.get(user = player_username)
# 	except Exception, e:
# 		return HttpResponse('This user does not exist')
	

# 	band.members.remove(player)
# 	band.save()

# 	return HttpResponseRedirect('/bandmatch/band/band_name_slug/edit')


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


def get_profileDetails(request, username):
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
	if player.privacy == 1 and request.user != user: # if 1 is on and 0 is off
		context_dict['email'] = user.email #only displayed for registered users and if user allows it
		context_dict['contact_info'] = player.contact_info 
		context_dict['location'] = player.location
	else:
		context_dict['email'] = ''
		context_dict['contact_info'] =  ''
		context_dict['location'] = player.location

	if player.demo:
		context_dict['demo'] = player.demo.url #not sure if this is how you get a file url
	else:
		context_dict['demo']= ''

	if player.image:
		context_dict['pic'] = player.image.url
	else:
		context_dict['pic'] = ''

	return context_dict

#Displayes the user profile, and allows modification if its the user's own page
def profile(request, username): #could possibly use user_id here
	context_dict = {}

	# user = User.objects.get(username = username)

	# player = Player.objects.get(user = user)

	# context_dict['username'] = username

	# context_dict['first_name'] = user.first_name

	# context_dict['last_name'] = user.last_name

	# context_dict['description'] = player.description

	# context_dict['instruments'] = player.instruments #should probably be checked how it works when instruments are a list

	# user_bands = player.band_set.all()

	# context_dict['bands'] = user_bands

	# #we could do this or pass privacy to the html with the context_dict
	# #and choose what to display there
	# if player.privacy == 1 and request.user != user: # if 1 is on and 0 is off
	# 	context_dict['email'] = user.email #only displayed for registered users and if user allows it
	# 	context_dict['contact_info'] = player.contact_info 
	# 	context_dict['location'] = player.location
	# else:
	# 	context_dict['email'] = ''
	# 	context_dict['contact_info'] =  ''
	# 	context_dict['location'] = ''

	# if player.demo:
	# 	context_dict['demo'] = player.demo.url #not sure if this is how you get a file url
	# else:
	# 	context_dict['demo']= ''

	# if player.image:
	# 	context_dict['pic'] = player.image.url
	# else:
	# 	context_dict['pic'] = ''

	context_dict = get_profileDetails(request, username)

	user = User.objects.get(username = username)

	player = Player.objects.get(user = user)

	#can use this in html to display link to edit profile
	if request.user == user:
		context_dict['is_user'] = 1
	else:
		context_dict['is_user'] = 0

        #JUST TO MAKE SURE MY LOCATION IS SHOWN
        context_dict['location'] = player.location
	return render(request, 'bandmatch/profile.html', context_dict)

#Might not be necessary.
def edit_profile(request, username):
	context_dict = {}

	# user = User.objects.get(username = username)

	# player = Player.objects.get(user = user)

	# context_dict['username'] = username

	# context_dict['first_name'] = user.first_name

	# context_dict['last_name'] = user.last_name

	# context_dict['description'] = player.description

	# context_dict['instruments'] = player.instruments 

	# user_bands = player.band_set.all()

	# context_dict['bands'] = user_bands

	# if player.privacy == 1 and request.user != user: # more security ftw!
	# 	context_dict['email'] = user.email 
	# 	context_dict['contact_info'] = player.contact_info 
	# 	context_dict['location'] = player.location
	# else:
	# 	context_dict['email'] = ''
	# 	context_dict['contact_info'] =  ''
	# 	context_dict['location'] = ''

	# if player.demo:
	# 	context_dict['demo'] = player.demo.url #not sure if this is how you get a file url
	# else:
	# 	context_dict['demo']= ''

	# if player.image:
	# 	context_dict['pic'] = player.image.url
	# else:
	# 	context_dict['pic'] = ''

	context_dict = get_profileDetails(request, username)

	user = User.objects.get(username = username)

	player = Player.objects.get(user = user)

	if request.user == user:
		context_dict['is_user'] = 1
	else:
		context_dict['is_user'] = 0
 
	context_dict['user_form'] = UserForm(instance = user)
	context_dict['player_form'] = PlayerForm(instance = player)

	if request.method == 'POST':
        # Attempt to grab information from the raw form information.
		user_form = UserForm(request.POST, request.FILES, instance= user)
		player_form = PlayerForm(request.POST, request.FILES, instance= player)

		instruments_list = player_form.data['instruments'].encode('ascii', 'ignore').lower().split(",")
		for i in range(len(instruments_list)):
			instruments_list[i] = re.sub(r"[^a-z]+", '', instruments_list[i])
		player_form.data['instruments'] = instruments_list

		if user_form.is_valid() and player_form.is_valid():
			
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			player = player_form.save(commit=False)
			player.user = user  #do we need that here


			#Demo? Picture?

			if 'image' in request.FILES:
				profile.image = request.FILES['image']

			if 'demo' in request.FILES:
				profile.demo = request.FILES['demo']

			player.save()

			context_dict.update(get_profileDetails(request, username))

		else:
			print user_form.errors, player_form.errors

	return render(request, 'bandmatch/edit_profile.html', context_dict)


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

    context_dict = {}

    result_list = []

    context_dict["resultsp"] = result_list
    context_dict["resultsb"] = result_list
    
    if request.method == 'POST':
		if request.POST["submit"] == "Search Players":
			player_username_query = request.POST["player_username_query"]
			player_name_query = request.POST["player_name_query"]
			player_instrument_query = request.POST["player_instrument_query"]
			player_location_query = request.POST["player_location_query"]

			context_dict["player_username_query"] = player_username_query
			context_dict["player_name_query"] = player_name_query
			context_dict["player_instrument_query"] = player_instrument_query
			context_dict["player_location_query"] = player_location_query

			players_list =  Player.objects.all()

			if player_username_query != "":
				players_list =  players_list.filter(user__username__contains = player_username_query)

			if player_location_query != "":
				players_list = players_list.filter(location__contains = player_location_query)

			if player_name_query != "":
				players_list_f = players_list.filter(user__first_name__contains = player_name_query)
				players_list_l = players_list.filter(user__last_name__contains = player_name_query)
				for p in players_list_f:
					if p not in result_list:
						result_list.append(p)
				for p in players_list_l:
					if p not in result_list:
						result_list.append(p)
			else:
				for p in players_list:
					if p not in result_list:
						result_list.append(p)

			
			if player_instrument_query != "":
				players_list_instr = Player.objects.all()
				result_list_instr = []
				for player in players_list_instr:
					if player_instrument_query in player.instruments and player in result_list:
						result_list_instr.append(player)

				result_list = result_list_instr

			context_dict["resultsp"] = result_list

		if request.POST["submit"] == "Search Bands":
			band_name_query = request.POST["band_name_query"]
			band_looking_for_query = request.POST["band_looking_for_query"]
			band_location_query = request.POST["band_location_query"]

			context_dict["band_name_query"] = band_name_query
			context_dict["band_looking_for_query"] = band_looking_for_query
			context_dict["band_location_query"] = band_location_query

			bands_list = Band.objects.all()

			if band_name_query != "":
				bands_list = bands_list.filter(name__contains = band_name_query)
			if band_location_query != "":
				bands_list = bands_list.filter(location__contains = band_location_query)
				for b in bands_list:
					result_list.append(b)

			if band_looking_for_query != "":
				result_list_ad = []
				adverts_list = Advert.objects.filter(looking_for__contains = band_looking_for_query)
				for ad in adverts_list:
					if ad.band in result_list:
						result_list_ad.append(ad.band)

				result_list = result_list_ad

			context_dict["results"] = result_list

    return render(request, 'bandmatch/advanced_search.html', context_dict)


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

        return render(request, 'bandmatch/user_list.html', {'user_list': user_list })


def suggest_member(request, band_name_slug):
	band = Band.objects.get(slug = band_name_slug)
	user_list = []
	starts_with = ''

	if request.method == 'GET':
		starts_with = request.GET['suggest_mem']

	if starts_with != '':
		user_list = band.members.all().filter(user__username__istartswith = starts_with)

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



"""
Messages still has some inconsistancies:

1) If you fill all the fields and click "add player", the message is sent.
2) After sending a message and clicking back the previous information is saved.
3) Needs a way to remove recipiants.

1) Could be fixed by changing the order of request.POST.__contains__ and message_form.is_valid

"""

#A view to send a message for one or many users
@login_required
def send_message(request, reciever_list=[]):
	context_dict = {}
	if request.method == 'POST':
		#Either send the message or do other stuff

		message_form = MessageForm(request.POST)

		if request.POST.__contains__('suggestion'):
			#Add the added reciever to list
			new_recipiant = request.POST['suggestion']
			if new_recipiant not in reciever_list: #Not adding dublicates
				reciever_list.append(new_recipiant)
			#Pass the list to the view, which will pass it back if a new reciever is added
			context_dict['reciever_list'] = reciever_list
		#Chech if the title and content have been added
		if message_form.is_valid():
			#Check if the're recievers for the message
			if (len(reciever_list) > 0):
				message = message_form.save(commit = False)
				user = request.user
				message.sender = Player.objects.get(user = user)
				message.save()

			#add recievers to the message recievers
				for reciever in reciever_list:
					try:
						recipiant = Player.objects.get(user__username = reciever)
						message.recipients.add(recipiant)
					except:
						pass

				message.save()
				#Return a different view so the reciever_list gets wiped.
				return(HttpResponseRedirect(reverse('display_messages')))
			else:
				#No recipiants. Don't send the message. Tell the user to add recipiants.
				messages.add_message(request, messages.INFO, 'Please add a recipiant to send a message.')
		else:
			#The form wasn't valid.
			messages.add_message(request, messages.INFO, 'Please add a title and content to send a message.')




	message_draft = MessageForm()

	context_dict['message_draft'] = message_draft
	return render(request, "bandmatch/send_message.html", context_dict)
