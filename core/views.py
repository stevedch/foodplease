from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse

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
    cart_ids = request.session.get('cart', [])
    items = MenuItem.objects.filter(id__in=cart_ids)
    total = sum(item.price for item in items)
    return render(request, 'core/cart.html', {'items': items, 'total': total})


@require_POST
def remove_from_cart(request, item_id):
    cart = request.session.get('cart', [])
    if item_id in cart:
        cart.remove(item_id)
        request.session['cart'] = cart
    return redirect('cart_list')


@require_POST
def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart_list')


## API
def add_to_order(request, item_id):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        if item_id not in cart:
            cart.append(item_id)
            request.session['cart'] = cart
    return redirect('menu_list')

def cart_count(request):
    cart = request.session.get('cart', [])
    return JsonResponse({'count': len(cart)})
