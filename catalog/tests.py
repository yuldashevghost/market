from django.test import TestCase
from django.urls import reverse
from .models import Category, Product, Tag


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=99.99,
            stock=10,
            category=self.category
        )
    
    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.is_in_stock())
    
    def test_product_out_of_stock(self):
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock())
    
    def test_product_slug_auto_generation(self):
        product = Product.objects.create(
            name='New Product',
            description='Test',
            price=50.00,
            stock=5,
            category=self.category
        )
        self.assertEqual(product.slug, 'new-product')


class ProductListViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        for i in range(15):
            Product.objects.create(
                name=f'Product {i}',
                slug=f'product-{i}',
                price=10.00 + i,
                stock=10,
                category=self.category
            )
    
    def test_product_list_view(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product')
    
    def test_product_list_pagination(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('products' in response.context)
        self.assertEqual(len(response.context['products']), 12)  # Default page size
    
    def test_product_list_filtering(self):
        response = self.client.get(reverse('catalog:product_list'), {'category': 'electronics'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_category'], 'electronics')
    
    def test_product_list_search(self):
        response = self.client.get(reverse('catalog:product_list'), {'q': 'Product 1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')


class ProductDetailViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            price=99.99,
            stock=10,
            category=self.category
        )
    
    def test_product_detail_view(self):
        response = self.client.get(reverse('catalog:product_detail', args=['test-product']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

