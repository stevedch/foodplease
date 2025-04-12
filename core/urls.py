from django.urls import path

from . import views
from . import api

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('menu/', views.menu_view, name='menu_view'),
    path('cart/', views.cart_view, name='cart_view'),
    path('orders/history/', views.order_history_view, name='order_history_view'),
    path('profile/', views.user_profile_view, name='user_profile_view'),

    # api
    path('cart/add/<int:item_id>/', api.add_to_order, name='add_to_order'),
    path('cart/remove/<int:item_id>/', api.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', api.clear_cart, name='clear_cart'),
    path('cart/count/', api.cart_count, name='cart_count'),
]
