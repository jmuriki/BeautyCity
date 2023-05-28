from django.urls import path
from service import views

urlpatterns = [
    path('', views.index, name='main_page'),
    path('contacts/', views.contacts, name='contacts'),
    path('masters/', views.masters, name='masters'),
    path('reviews/', views.reviews, name='reviews'),
    path('services/', views.services, name='services'),
    path('admin_front/', views.admin, name='admin_front'),
    path('notes/', views.notes, name='notes'),
    path('popup/', views.popup, name='popup'),
    path('service/', views.service, name='service'),
    path('serviceFinally/', views.serviceFinally, name='serviceFinally'),
    path('payment/', views.payment, name='payment'),
    path('pay_result/', views.pay_result, name='pay_result'),
    path('get_masters/', views.get_masters, name='get_masters'),
    path('get_available_time/', views.get_available_time, name='get_available_time')
]
