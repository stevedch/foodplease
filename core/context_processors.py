def cart_item_count(request):
    cart = request.session.get("cart", [])
    if isinstance(cart, list):
        total_quantity = sum(item.get("quantity", 0) for item in cart)
    else:
        total_quantity = 0
    return {
        "cart_item_count": total_quantity
    }
