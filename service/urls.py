from django.urls import path
from service import views

urlpatterns = [
    path('', views.index),
    path('admin_front/', views.admin),
    path('notes/', views.notes),
    path('popup/', views.popup),
    path('service/', views.service),
    path('serviceFinally/', views.serviceFinally),
]
