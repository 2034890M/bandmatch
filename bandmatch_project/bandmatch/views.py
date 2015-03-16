from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from bandmatch.models import Band, Player, Message, Advert, User
from bandmatch.forms import UserForm, PlayerForm, BandForm

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

	return render(request, 'bandmatch/band.html', context_dict)

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

			if 'demo' in request.FILES:
				newband.demo = request.FILES['demo']

			context_dict['created'] = True
			#A redirection to the created band's site would be nice
			#Is there a more elegant way?
			url = '/bandmatch/band/' #Hardcoded! Bad :((
			url = url + newband.name
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

	context_dict['first name'] = user.first_name

	context_dict['last name'] = user.last_name

	context_dict['description'] = player.description

	context_dict['instruments'] = player.instrument #should probably be checked how it works when instruments are a list

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
	#should only search in bands, might be able to do it without bing, maybe not
	return render(request, 'bandmatch/search_bands.html', {})

def search_players(request):
	return render(request, 'bandmatch/search_players.html', {})

@login_required
def user_logout(request):
    #Since we know the user is logged in, we can now just log them out.
   logout(request)

    #Take the user back to the homepage.
   return HttpResponseRedirect('/rango/')

	