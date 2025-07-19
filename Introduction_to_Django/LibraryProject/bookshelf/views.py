from django.shortcuts import render
from django.http import HttpResponse

def index(request): return HttpResponse("Welcome to my book shelf.")
# Create your views here.
