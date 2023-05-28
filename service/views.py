import os
import uuid

from urllib.parse import urlparse
from datetime import date, datetime
from yookassa import Configuration, Payment

from django.http import HttpResponse
from django.shortcuts import render, redirect
from beauty_city.settings import PAY_ACC, PAY_KEY
from service.models import (
	Order,
	Salon,
	Category,
	Service,
	Specialist,
	Client,
	WorkDay,
	TimeSlot,
)


def save_to_cookies(request, key, payload):
	request.session[key] = payload
	request.session.modified = True
	response = HttpResponse("Your choice was saved as a cookie!")
	response.set_cookie('session_id', request.session.session_key)
	return response


def index(request):
	return render(request, 'index.html')


def contacts(request):
	return render(request, 'contacts.html')


def reviews(request):
	return render(request, 'reviews.html')


def masters(request):
	return render(request, 'masters.html')


def services(request):
	return render(request, 'services.html')


def admin(request):
	return render(request, 'admin_front.html')


def notes(request, client_id):
	today = date.today()
	client = Client.objects.get(id=client_id)
	past_orders = Order.objects.filter(
		client=client,
	)
	future_orders = Order.objects.filter(
		client=client,
	)
	context = {
		"client": client,
		"past_orders": past_orders,
		"future_orders": future_orders,
	}
	return render(request, 'notes.html', context)


def popup(request):
	return render(request, 'popup.html')


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


def serviceFinally(request):
	context = {'order': Order.objects.first()}
	if request.method == 'POST':
		context['selected_salon'] = request.POST.get('selected_salon')
		context['selected_address'] = request.POST.get('selected_address')
		context['selected_service'] = request.POST.get('selected_service')
		context['selected_price'] = request.POST.get('selected_price')
		context['selected_master'] = request.POST.get('selected_master')
		context['selected_speciality'] = request.POST.get('selected_speciality')
		context['selected_time'] = request.POST.get('selected_time')
		context['selected_date'] = request.POST.get('selected_date')
		context['selected_month'] = request.POST.get('selected_month')
		context['selected_year'] = request.POST.get('selected_year')
		context['new_order_number'] = Order.objects.count() + 1
		context['specialist'] = Specialist.objects.get(name=request.POST.get('selected_master'))
	return render(request, 'serviceFinally.html', context)


def order(request, context=None):
	if request.method == 'POST':
		specialist = Specialist.objects.get(
			name=request.POST.get('selected_master'),
		)
		client, _ = Client.objects.get_or_create(
			name=request.POST.get('client_input'),
			phone=request.POST.get('contact_input'),
		)
		work_day, _ = WorkDay.objects.get_or_create(
			date=datetime(
				int(request.POST.get('selected_year')),
				int(request.POST.get('selected_month')) + 1,
				int(request.POST.get('selected_date')),
			),
		)
		work_day.specialists.set([specialist])
		time_slot, _ = TimeSlot.objects.get_or_create(
			start_time=request.POST.get('selected_time'),
			date=work_day,
			specialist=specialist,
		)
		order, _ = Order.objects.get_or_create(
			client=client,
			procedure=Service.objects.get(name=request.POST.get('selected_service')),
			salon=Salon.objects.get(name=request.POST.get('selected_salon')),
			specialist=specialist,
			order_hour=time_slot,
			comment=request.POST.get('comment_input'),
		)
	return redirect('/notes/{}'.format(client.id))


def make_pay(pay_account, pay_secretkey, amount, payment_descr, ret_url):
	Configuration.account_id = pay_account
	Configuration.secret_key = pay_secretkey
	return Payment.create({
		"amount": {
			"value": amount,
			"currency": "RUB"
		},
		"confirmation": {
			"type": "redirect",
			"return_url": ret_url
		},
		"capture": True,
		"description": payment_descr
		})


def payment(request):
	if request.method == 'POST':
		order_id = request.POST.get('order_id')
		order = Order.objects.get(id=order_id)
		payment_descr = "Оплата услуги салона красоты"
		amount = order.procedure.price
		save_to_cookies(request, 'paid_order_id', order_id)
		absolute_url = request.build_absolute_uri()
		parsed_url = urlparse(absolute_url)
		ret_url = f'{parsed_url.scheme}://{parsed_url.netloc}/pay_result?payment_success=1'
		yookassa = make_pay(PAY_ACC, PAY_KEY, amount, payment_descr, ret_url)
		return redirect(yookassa.confirmation.confirmation_url)


def pay_result(request, context={}):
	payment_res = request.GET['payment_success']
	message = "Оплата не прошла."
	if payment_res:
		message = "Оплата прошла успешно."
		paid_order_id = request.session.get('paid_order_id')
		paid_order = Order.objects.get(id=paid_order_id)
		paid_order.payment_status = 'paid'
		paid_order.save()
		save_to_cookies(request, 'paid_order_id', None)
	context['payment_res'] = message
	return render(request, 'notes.html', context)
