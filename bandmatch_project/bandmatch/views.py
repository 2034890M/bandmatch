from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    context_dict = {}

    

    response = render(request,'bandmatch/index.html', context_dict)
    return response


def about(request):


	return render(request, 'bandmatch/about.html', {})


def your_bands(request):

	return render(request, 'bandmatch/your_bands.html', {})

def band(request):
	return render(request, 'bandmatch/band.html', {})


def add_band(request):
	return render(request, 'bandmatch/add_band.html', {})


def profile(request):
	return render(request, 'bandmatch/profile.html', {})

def edit_profile(request):
	return HttpResponse("Template missing")

def register_profile(request):
	HttpResponse("Template missing")

def search_bands(request):
	return render(request, 'bandmatch/search_bands.html', {})

def search_players(request):
	return render(request, 'bandmatch/search_players.html', {})

	