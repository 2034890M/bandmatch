from django.shortcuts import render
from django.http import HttpResponse
from bandmatch.models import Band

# Create your views here.
def index(request):

    context_dict = {}

    band_list = Band.objects.order_by('name')[:5]

    context_dict['bands'] = band_list

    response = render(request,'bandmatch/index.html', context_dict)
    return response


def about(request):


	return render(request, 'bandmatch/about.html', {})


def your_bands(request):

	return render(request, 'bandmatch/your_bands.html', {})

def band(request, band_name_slug):
	band = Band.objects.get(slug = band_name_slug)
	band_name = band.name
	return render(request, 'bandmatch/band.html', {'name': band_name})


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

	