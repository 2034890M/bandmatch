from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):

    context_dict = {}

    

    response = render(request,'bandmatch/index.html', context_dict)
