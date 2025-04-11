from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.product_list, name='product_list'),
    path('order/', views.create_order, name='create_order'),
    path('orders/history/', views.order_history, name='order_history'),
    path('profile/', views.user_profile, name='user_profile'),
]
