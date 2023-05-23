import os

from django.shortcuts import render


def index(request, context=None):
	return render(request, 'index.html', context)


def contacts(request, context=None):
	return render(request, 'contacts.html', context)


def reviews(request, context=None):
	return render(request, 'reviews.html', context)


def masters(request, context=None):
	return render(request, 'masters.html', context)


def services(request, context=None):
	return render(request, 'services.html', context)


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
