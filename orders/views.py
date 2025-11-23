from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


@login_required
def order_create(request):
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Validate stock before creating order
                for item in cart:
                    product = item['product']
                    quantity = item['quantity']
                    if product.stock < quantity:
                        messages.error(request, f'Sorry, only {product.stock} {product.name} available.')
                        return redirect('cart:cart_detail')
                
                # Create order
                order = form.save(commit=False)
                order.user = request.user
                order.total_amount = cart.get_total()
                order.save()
                
                # Create order items and update stock
                for item in cart:
                    product = item['product']
                    quantity = item['quantity']
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        product_name=product.name,
                        price_at_purchase=product.price,
                        quantity=quantity
                    )
                    # Update stock
                    product.stock -= quantity
                    product.save()
                
                # Clear cart
                cart.clear()
                
                messages.success(request, f'Order #{order.id} has been placed successfully!')
                return redirect('orders:order_detail', order_id=order.id)
    else:
        # Pre-fill form with user profile if available
        initial = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial = {
                'shipping_address': profile.address,
                'shipping_city': profile.city,
                'shipping_state': profile.state,
                'shipping_zip': profile.zip_code,
                'shipping_country': profile.country,
            }
        form = OrderCreateForm(initial=initial)
    
    return render(request, 'orders/order_create.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

