from django.test import TestCase, RequestFactory
from catalog.models import Category, Product
from .cart import Cart


class CartTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=99.99,
            stock=10,
            category=self.category
        )
    
    def test_cart_add(self):
        request = self.factory.get('/')
        request.session = {}
        cart = Cart(request)
        cart.add(self.product, quantity=2)
        
        self.assertEqual(len(cart), 2)
        self.assertEqual(float(cart.get_total()), 199.98)
    
    def test_cart_remove(self):
        request = self.factory.get('/')
        request.session = {}
        cart = Cart(request)
        cart.add(self.product)
        cart.remove(self.product)
        
        self.assertEqual(len(cart), 0)
        self.assertEqual(cart.get_total(), 0)
    
    def test_cart_update_quantity(self):
        request = self.factory.get('/')
        request.session = {}
        cart = Cart(request)
        cart.add(self.product, quantity=1)
        cart.add(self.product, quantity=2, override_quantity=True)
        
        self.assertEqual(len(cart), 2)

