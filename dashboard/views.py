from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from orders.models import Order


@staff_member_required
def order_list(request):
    orders = Order.objects.all().select_related('user').prefetch_related('items')
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    return render(request, 'dashboard/order_list.html', {
        'orders': orders,
    })

