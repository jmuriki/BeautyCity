import os

from django.shortcuts import render

from service.models import Salon, Category, Service, Specialist


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
	return render(request, 'admin_front.html', context)


def notes(request, context=None):
	return render(request, 'notes.html', context)


def popup(request, context=None):
	return render(request, 'popup.html', context)


def service(request, context=None):
	salons = Salon.objects.prefetch_related("workers")
	categories = Category.objects.prefetch_related("services")
	masters = Specialist.objects.all()
	context = {
		"salons": salons,
		"categories": categories,
		"masters": masters,
	}
	return render(request, 'service.html', context)


def serviceFinally(request, context=None):
	if request.method == 'POST':
		print("!!!", "POST")
	# 	selected_time = request.POST.get('selected_time')
	# 	select_salon = request.POST.get('selectSalon')
	# 	select_service = request.POST.get('selectService')
	# 	select_master = request.POST.get('selectMaster')
	return render(request, 'serviceFinally.html', context)
