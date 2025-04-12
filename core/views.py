from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import MenuItem, User, Order


def home(request):
    return render(request, 'core/home.html')


def menu_list(request):
    menu_items = MenuItem.objects.all()
    return render(request, 'core/menu_list.html', {'menu_items': menu_items})


def create_order(request):
    users = User.objects.all()
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        item_ids = request.POST.getlist('products')
        user = get_object_or_404(User, id=user_id)
        selected_items = MenuItem.objects.filter(id__in=item_ids)
        total = sum(item.price for item in selected_items)

        order = Order.objects.create(user=user, total_amount=total, order_date=timezone.now())
        order.menu_items.set(selected_items)
        order.save()

        return render(request, 'core/order_success.html', {'order': order})

    return render(request, 'core/create_order.html', {
        'users': users,
        'menu_items': menu_items
    })


def order_history(request):
    orders = Order.objects.select_related('user').prefetch_related('menu_items').all()
    return render(request, 'core/order_history.html', {'orders': orders})


def user_profile(request):
    users = User.objects.all()
    return render(request, 'core/user_profile.html', {'users': users})


def view_cart(request):
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
    return render(request, 'core/cart.html', {
        'items': items,
        'total': total
    })


@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    updated_cart = []

    for item in cart:
        if item["menu_id"] == item_id:
            if item["quantity"] > 1:
                item["quantity"] -= 1
                updated_cart.append(item)
        else:
            updated_cart.append(item)
    request.session['cart'] = updated_cart
    return redirect('cart_list')


@require_POST
def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart_list')


## API
def add_to_order(request, item_id):
    if request.method == 'POST':
        qty = int(request.GET.get('qty', 1))
        cart = request.session.get('cart', [])
        if isinstance(cart, dict):
            cart = [{"menu_id": int(k), "quantity": v} for k, v in cart.items()]

        for item in cart:
            if item["menu_id"] == item_id:
                item["quantity"] += qty
                break
        else:
            cart.append({
                "menu_id": item_id,
                "quantity": qty
            })
        request.session['cart'] = cart
    return redirect('menu_list')


def cart_count(request):
    cart = request.session.get('cart', [])
    total_quantity = sum(item.get('quantity', 0) for item in cart if isinstance(item, dict))
    return JsonResponse({'count': total_quantity})
