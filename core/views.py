
from django.shortcuts import render, get_object_or_404
from .models import Product, User, Order
from decimal import Decimal
from django.utils import timezone


def home(request):
    return render(request, 'core/home.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})


def create_order(request):
    users = User.objects.all()
    products = Product.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        product_ids = request.POST.getlist('products')
        user = get_object_or_404(User, id=user_id)
        selected_products = Product.objects.filter(id__in=product_ids)
        total = sum(p.price for p in selected_products)

        order = Order.objects.create(user=user, total_amount=total, order_date=timezone.now())
        order.products.set(selected_products)
        order.save()

        return render(request, 'core/order_success.html', {'order': order})

    return render(request, 'core/create_order.html', {
        'users': users,
        'products': products
    })


def order_history(request):
    orders = Order.objects.select_related('user').prefetch_related('products').all()
    return render(request, 'core/order_history.html', {'orders': orders})


def user_profile(request):
    users = User.objects.all()
    return render(request, 'core/user_profile.html', {'users': users})