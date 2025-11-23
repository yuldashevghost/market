from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
]

