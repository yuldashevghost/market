from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, available=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if product.is_in_stock():
        cart.add(product, quantity=quantity)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'item_count': cart.get_item_count(),
                'total': str(cart.get_total())
            })
        return redirect('cart:cart_detail')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Product out of stock'}, status=400)
        return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        if product.stock >= quantity:
            cart.add(product, quantity=quantity, override_quantity=True)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'item_count': cart.get_item_count(),
                    'total': str(cart.get_total()),
                    'subtotal': str(product.price * quantity)
                })
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': f'Only {product.stock} items available'
                }, status=400)
    else:
        cart.remove(product)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'item_count': cart.get_item_count(),
                'total': str(cart.get_total())
            })
    
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'item_count': cart.get_item_count(),
            'total': str(cart.get_total())
        })
    
    return redirect('cart:cart_detail')


def cart_summary(request):
    cart = Cart(request)
    return JsonResponse({
        'item_count': cart.get_item_count(),
        'total': str(cart.get_total())
    })

