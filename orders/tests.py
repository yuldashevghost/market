from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Category, Product
from .models import Order, OrderItem


class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=99.99,
            stock=10,
            category=self.category
        )
        self.order = Order.objects.create(
            user=self.user,
            total_amount=99.99,
            shipping_address='123 Test St',
            shipping_city='Test City',
            shipping_state='TS',
            shipping_zip='12345',
            shipping_country='USA'
        )
    
    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.total_amount, 99.99)
        self.assertEqual(self.order.status, 'PENDING')
    
    def test_order_item_creation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            price_at_purchase=self.product.price,
            quantity=1
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.get_subtotal(), 99.99)
    
    def test_order_total_calculation(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            product_name=self.product.name,
            price_at_purchase=self.product.price,
            quantity=2
        )
        # Order total should be set at creation, but items subtotal should be correct
        item = OrderItem.objects.get(order=self.order)
        self.assertEqual(item.get_subtotal(), 199.98)


class CheckoutFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=99.99,
            stock=10,
            category=self.category
        )
    
    def test_checkout_requires_login(self):
        response = self.client.get('/orders/create/')
        self.assertRedirects(response, '/accounts/login/?next=/orders/create/')
    
    def test_checkout_creates_order(self):
        # Add to cart
        session = self.client.session
        session['cart'] = {str(self.product.id): {'quantity': 1, 'price': str(self.product.price)}}
        session.save()
        
        # Login
        self.client.login(username='testuser', password='testpass123')
        
        # Checkout
        response = self.client.post('/orders/create/', {
            'shipping_address': '123 Test St',
            'shipping_city': 'Test City',
            'shipping_state': 'TS',
            'shipping_zip': '12345',
            'shipping_country': 'USA'
        })
        
        # Should create order and redirect
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.items.count(), 1)

