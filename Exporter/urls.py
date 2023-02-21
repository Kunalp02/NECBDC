from django.contrib import admin
from django.urls import path, include
from . import views



urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ExporterLogin/', views.ExporterLogin, name='ExporterLogin'),
    path('ExporterSignup/', views.ExporterSignup, name='ExporterSignup'),
    path('Exporterlogout/', views.Exporterlogout, name='Exporterlogout'),
    path('dashboard/export_request/', views.export_request, name='export_request'),
    path('dashboard/get_types/', views.get_types, name='get_types'),
    path('dashboard/import_supply/', views.import_supply, name='import_supply'),
    path('dashboard/request_status/', views.request_status, name='request_status'),
    path('dashboard/orders/', views.orders, name='orders'),
    path('dashboard/stocks/', views.stocks, name='stocks'),
    path('dashboard/payments/', views.payments, name='payments'),
    path('dashboard/payments/send_payment_link/<order_number>/', views.send_payment_link, name='send_payment_link'),
    path('dashboard/payments/invoice/<order_number>/', views.invoice, name='invoice'),
    path('dashboard/profile/', views.profile, name='profile'),
    path('dashboard/profile/change_password/', views.change_password, name='change_password'),
    path('dashboard/profile/delete_account/', views.delete_account, name='delete_account'),
]
