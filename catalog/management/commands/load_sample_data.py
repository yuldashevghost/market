from django.core.management.base import BaseCommand
from catalog.models import Category, Tag, Product
from decimal import Decimal


class Command(BaseCommand):
    help = 'Load sample data for the marketplace'

    def handle(self, *args, **options):
        # Create categories
        electronics = Category.objects.get_or_create(name='Electronics', slug='electronics')[0]
        clothing = Category.objects.get_or_create(name='Clothing', slug='clothing')[0]
        books = Category.objects.get_or_create(name='Books', slug='books')[0]
        home = Category.objects.get_or_create(name='Home & Garden', slug='home-garden')[0]
        
        # Create tags
        tag_new = Tag.objects.get_or_create(name='New', slug='new')[0]
        tag_sale = Tag.objects.get_or_create(name='Sale', slug='sale')[0]
        tag_popular = Tag.objects.get_or_create(name='Popular', slug='popular')[0]
        tag_featured = Tag.objects.get_or_create(name='Featured', slug='featured')[0]
        
        # Create products
        products_data = [
            {
                'name': 'Wireless Headphones',
                'slug': 'wireless-headphones',
                'description': 'High-quality wireless headphones with noise cancellation',
                'price': Decimal('79.99'),
                'stock': 50,
                'category': electronics,
                'tags': [tag_new, tag_popular]
            },
            {
                'name': 'Smart Watch',
                'slug': 'smart-watch',
                'description': 'Feature-rich smartwatch with fitness tracking',
                'price': Decimal('199.99'),
                'stock': 30,
                'category': electronics,
                'tags': [tag_new, tag_featured]
            },
            {
                'name': 'Cotton T-Shirt',
                'slug': 'cotton-tshirt',
                'description': 'Comfortable 100% cotton t-shirt',
                'price': Decimal('19.99'),
                'stock': 100,
                'category': clothing,
                'tags': [tag_sale]
            },
            {
                'name': 'Denim Jeans',
                'slug': 'denim-jeans',
                'description': 'Classic fit denim jeans',
                'price': Decimal('49.99'),
                'stock': 75,
                'category': clothing,
                'tags': [tag_popular]
            },
            {
                'name': 'Python Programming Book',
                'slug': 'python-book',
                'description': 'Comprehensive guide to Python programming',
                'price': Decimal('29.99'),
                'stock': 40,
                'category': books,
                'tags': [tag_popular]
            },
            {
                'name': 'Django Web Development',
                'slug': 'django-book',
                'description': 'Learn Django framework for web development',
                'price': Decimal('34.99'),
                'stock': 35,
                'category': books,
                'tags': [tag_new]
            },
            {
                'name': 'Coffee Maker',
                'slug': 'coffee-maker',
                'description': 'Programmable coffee maker with timer',
                'price': Decimal('89.99'),
                'stock': 25,
                'category': home,
                'tags': [tag_featured]
            },
            {
                'name': 'Garden Tools Set',
                'slug': 'garden-tools',
                'description': 'Complete set of gardening tools',
                'price': Decimal('59.99'),
                'stock': 20,
                'category': home,
                'tags': [tag_sale]
            },
            {
                'name': 'Laptop Stand',
                'slug': 'laptop-stand',
                'description': 'Ergonomic aluminum laptop stand',
                'price': Decimal('39.99'),
                'stock': 60,
                'category': electronics,
                'tags': [tag_popular]
            },
            {
                'name': 'USB-C Cable',
                'slug': 'usb-c-cable',
                'description': 'Fast charging USB-C cable, 6ft',
                'price': Decimal('12.99'),
                'stock': 200,
                'category': electronics,
                'tags': [tag_sale]
            },
            {
                'name': 'Winter Jacket',
                'slug': 'winter-jacket',
                'description': 'Warm and waterproof winter jacket',
                'price': Decimal('129.99'),
                'stock': 45,
                'category': clothing,
                'tags': [tag_featured]
            },
            {
                'name': 'JavaScript Guide',
                'slug': 'javascript-guide',
                'description': 'Complete guide to modern JavaScript',
                'price': Decimal('27.99'),
                'stock': 50,
                'category': books,
                'tags': [tag_popular]
            },
        ]
        
        for product_data in products_data:
            tags = product_data.pop('tags')
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults=product_data
            )
            if created:
                product.tags.set(tags)
                self.stdout.write(
                    self.style.SUCCESS(f'Created product: {product.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Product already exists: {product.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully loaded {len(products_data)} products')
        )

