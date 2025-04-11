from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu_list, name='menu_list'),
    path('order/', views.create_order, name='create_order'),
    path('orders/history/', views.order_history, name='order_history'),
    path('profile/', views.user_profile, name='user_profile'),

    path('cart/', views.view_cart, name='cart_list'),

    # api
    path('cart/add/<int:item_id>/', views.add_to_order, name='add_to_order'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/count/', views.cart_count, name='cart_count'),
]
