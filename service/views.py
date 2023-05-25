import os
import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponse
from service.models import Order
from beauty_city.settings import PAY_ACC, PAY_KEY

from urllib.parse import urlparse
from yookassa import Configuration, Payment


def save_to_cookies(request, key, payload):
    request.session[key] = payload
    request.session.modified = True
    response = HttpResponse("Your choice was saved as a cookie!")
    response.set_cookie('session_id', request.session.session_key)
    return response

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
	if request.POST:
		order_id = int(request.POST.get('order_id'))
		payment_descr = request.POST.get('payment_descr')
		order = Order.objects.get(id=order_id)
		amount = order.procedure.price

		absolute_url = request.build_absolute_uri()
		parsed_url = urlparse(absolute_url)
		ret_url = f'{parsed_url.scheme}://{parsed_url.netloc}/pay_result?payment_success=1'
		print(ret_url)
		yookassa = make_pay(PAY_ACC, PAY_KEY, amount, payment_descr, ret_url)
		return redirect(yookassa.confirmation.confirmation_url)
	return redirect('serviceFinally')

def pay_result(request, context={}):
	payment_res = request.GET['payment_success']
	print(payment_res)
	message = "Оплата не прошла."
	if payment_res:
		message = "Оплата прошла успешно."
		paid_order_id = request.session.get('paid_order_id')
		paid_order = Order.objects.get(id=paid_order_id)
		paid_order.payment_status = 'paid'
		paid_order.save()
		save_to_cookies(request, 'paid_order_id', None)
	context['payment_res'] = message
	return render(request, 'pay_result.html', context)
