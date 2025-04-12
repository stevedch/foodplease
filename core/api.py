from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST


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
    return redirect('cart_view')


@require_POST
def clear_cart(request):
    request.session['cart'] = []
    return redirect('cart_view')


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
    return redirect('menu_view')


def cart_count(request):
    cart = request.session.get('cart', [])
    total_quantity = sum(item.get('quantity', 0) for item in cart if isinstance(item, dict))
    return JsonResponse({'count': total_quantity})
