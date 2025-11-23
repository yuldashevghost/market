#!/bin/bash
# Setup script for Django E-Commerce Marketplace

echo "Setting up Django E-Commerce Marketplace..."
echo ""

# Check if running as root (for apt commands)
if [ "$EUID" -ne 0 ]; then 
    echo "Note: Some commands require sudo privileges."
    echo "Please run: sudo apt install python3-venv python3-pip"
    echo ""
fi

# Install required system packages
echo "Step 1: Installing system packages..."
sudo apt update
sudo apt install -y python3-venv python3-pip

# Create virtual environment
echo ""
echo "Step 2: Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Step 3: Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo ""
echo "Step 4: Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations
echo ""
echo "Step 5: Running database migrations..."
python manage.py migrate

# Create media directory
echo ""
echo "Step 6: Creating media directory..."
mkdir -p media/products

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Load sample data: python manage.py load_sample_data"
echo "3. Run the server: python manage.py runserver"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source venv/bin/activate"

