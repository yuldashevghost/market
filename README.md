# Django E-Commerce Marketplace

A full-featured e-commerce web application built with Django, featuring server-rendered HTML templates, responsive design, and comprehensive shopping functionality.

## Features

- **Product Catalog**: Browse products with filtering, search, pagination, and sorting
- **Shopping Cart**: Add, update, and remove items with real-time total calculation
- **User Authentication**: Registration, login, logout, and password reset
- **Order Management**: Complete checkout flow with order tracking
- **User Profile**: View order history with real-time status updates
- **Admin Dashboard**: Manage orders and update order statuses
- **Responsive Design**: Optimized for desktop (≥1024px), tablet (768-1023px), and mobile (<768px)
- **Modern UI**: Green (#16A34A) and flame (#FF6A00) color scheme

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default, easily configurable for PostgreSQL/MySQL)
- **Frontend**: Django Templates, Vanilla CSS, Vanilla JavaScript
- **Image Handling**: Pillow

## Project Structure

```
market/
├── marketplace/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── catalog/              # Product catalog app
│   ├── models.py        # Product, Category, Tag models
│   ├── views.py         # Product listing and detail views
│   └── management/      # Management commands
├── cart/                # Shopping cart app
│   ├── models.py        # Cart and CartItem models
│   ├── cart.py          # Session-based cart utility
│   └── views.py         # Cart management views
├── orders/              # Order management app
│   ├── models.py        # Order and OrderItem models
│   └── views.py         # Checkout and order views
├── accounts/            # User accounts app
│   ├── models.py        # Profile model
│   └── views.py         # Authentication and profile views
├── dashboard/           # Admin dashboard app
│   └── views.py         # Order management views
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS)
│   ├── css/
│   └── js/
└── media/               # User-uploaded files (created on first upload)
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd market
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

6. **Load sample data (optional):**
   ```bash
   python manage.py load_sample_data
   ```
   This will create sample categories, tags, and products for testing.

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Environment Variables

For production deployment, create a `.env` file or set environment variables:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

Update `settings.py` to use environment variables:

```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production-xyz123')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
```

## Usage Guide

### For Customers

1. **Browse Products**: Visit the home page or products page to see available items
2. **Search & Filter**: Use the search bar or filter sidebar to find specific products
3. **View Product Details**: Click on any product to see details and add to cart
4. **Shopping Cart**: Add items to cart and adjust quantities
5. **Checkout**: Register/login, provide shipping address, and place order
6. **Track Orders**: View order history and status in your profile

### For Administrators

1. **Access Admin Panel**: Go to `/admin/` and login with superuser credentials
2. **Manage Products**: Add, edit, or remove products, categories, and tags
3. **Manage Orders**: View orders and update their status (PENDING → PROCESSING → DELIVERING → DELIVERED)
4. **Order Status Updates**: When you update an order status, customers will see the change in their profile immediately

## Key URLs

- `/` - Home page with featured products
- `/products/` - Product listing with filters
- `/products/<slug>/` - Product detail page
- `/cart/` - Shopping cart
- `/orders/create/` - Checkout page (requires login)
- `/orders/<id>/` - Order detail page
- `/profile/` - User profile with order history
- `/accounts/login/` - Login page
- `/accounts/register/` - Registration page
- `/accounts/password-reset/` - Password reset
- `/dashboard/orders/` - Admin order management (staff only)
- `/admin/` - Django admin panel

## Order Status Flow

1. **PENDING**: Order placed, awaiting processing
2. **PROCESSING**: Order is being prepared
3. **DELIVERING**: Order is out for delivery
4. **DELIVERED**: Order has been delivered
5. **CANCELLED**: Order has been cancelled

## Testing

Run the test suite:

```bash
python manage.py test
```

Test coverage includes:
- Model tests (product creation, stock management)
- View tests (product listing, filtering, pagination)
- Cart functionality tests
- Checkout flow tests

## Static Files and Media

- **Static files** (CSS, JS): Collected to `staticfiles/` directory
- **Media files** (product images): Stored in `media/` directory

To collect static files for production:

```bash
python manage.py collectstatic
```

## Database

The default database is SQLite (`db.sqlite3`). For production, configure PostgreSQL or MySQL in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Security Considerations

- CSRF protection is enabled on all forms
- Authentication required for checkout and profile pages
- Stock validation prevents overselling
- Admin-only access to order management
- Change `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` for production

## Customization

### Colors

Edit CSS variables in `static/css/style.css`:

```css
:root {
    --color-primary: #16A34A;      /* Green */
    --color-flame: #FF6A00;        /* Orange/Red */
}
```

### Pagination

Default products per page: 12. Change in `catalog/views.py`:

```python
paginator = Paginator(products, 12)  # Change 12 to desired number
```

## Troubleshooting

### Images not displaying
- Ensure `MEDIA_ROOT` and `MEDIA_URL` are configured in `settings.py`
- Check that the `media/` directory exists and is writable
- Verify image uploads are working in admin panel

### Cart not persisting
- Check that sessions are enabled in `settings.py`
- Verify `CART_SESSION_ID` is set correctly

### Static files not loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` in `settings.py`
- Ensure `django.contrib.staticfiles` is in `INSTALLED_APPS`

## License

This project is open source and available for educational and commercial use.

## Support

For issues or questions, please check the Django documentation or create an issue in the project repository.

