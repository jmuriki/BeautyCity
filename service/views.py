import os

from django.shortcuts import render

# Create your views here.

def index(request, context=None):
	return render(request, 'index.html', context)


def admin(request, context=None):
	return render(request, 'admin.html', context)


def notes(request, context=None):
	return render(request, 'notes.html', context)


def popup(request, context=None):
	return render(request, 'popup.html', context)


def service(request, context=None):
	return render(request, 'service.html', context)


def serviceFinally(request, context=None):
	return render(request, 'serviceFinally.html', context)
