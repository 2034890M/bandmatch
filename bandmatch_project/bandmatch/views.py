from django.shortcuts import render
from django.http import HttpResponse
from bandmatch.models import Band, Player, Message, Advert
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):

    context_dict = {}

    user = request.user

    if not user.is_authenticated():
    	return redurect('bandmatch/about/')

    recent_messages = user.message_set.all().order_by('date')[:5]

    context_dict['messages'] = recent_messages


    response = render(request,'bandmatch/index.html', context_dict)
    return response


def about(request):


	return render(request, 'bandmatch/about.html', {})


def your_bands(request):
	context_dict = {}

	user = request.user

	player = player = Player.objects.get(user = user)

	user_bands = player.band_set.all() #should get all the bands that have that user as a member

	context_dict['bands'] = user_bands

	return render(request, 'bandmatch/your_bands.html', context_dict)

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


def add_band(request):
	return render(request, 'bandmatch/add_band.html', {})


def profile(request, username): #could possibly use user_id here
	context_dict = {}

	user = User.objects.get(username = username)

	player = Player.objects.get(user = user)

	context_dict['first name'] = user.first_name

	context_dict['first name'] = user.last_name

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

def edit_profile(request):
	return HttpResponse("Template missing")

def register_profile(request):
	HttpResponse("Template missing")

def search_bands(request):
	#should only search in bands, might be able to do it without bing, maybe not
	return render(request, 'bandmatch/search_bands.html', {})

def search_players(request):
	return render(request, 'bandmatch/search_players.html', {})

	