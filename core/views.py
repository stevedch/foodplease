from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .models import MenuItem, User, Order


def home_view(request):
    return render(request, 'core/home_view.html')


def menu_view(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'core/menu_view.html', {'menu_items': menu_items})


def order_history_view(request):
    orders = Order.objects.select_related('user').prefetch_related('menu_items').all()
    return render(request, 'core/order_history_view.html', {'orders': orders})


def user_profile_view(request):
    users = User.objects.all()
    return render(request, 'core/user_profile_view.html', {'users': users})


def cart_view(request):
    cart = request.session.get('cart', [])
    items = []
    total = 0
    if isinstance(cart, dict):
        cart = [{"menu_id": int(k), "quantity": v} for k, v in cart.items()]
        request.session['cart'] = cart
    for entry in cart:
        if not isinstance(entry, dict) or "menu_id" not in entry:
            continue
        item = get_object_or_404(MenuItem, id=entry["menu_id"])
        quantity = entry.get("quantity", 1)
        item.quantity = quantity
        item.subtotal = item.price * quantity
        items.append(item)
        total += item.subtotal
    return render(request, 'core/cart_view.html', {
        'items': items,
        'total': total
    })