#!/bin/bash
# Quick run script (assumes setup is complete)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Please run ./setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "Django not found. Installing dependencies..."
    pip install -r requirements.txt
fi

# Run migrations (in case database doesn't exist)
python manage.py migrate --run-syncdb 2>/dev/null || python manage.py migrate

# Create media directory if it doesn't exist
mkdir -p media/products

# Run the development server
echo "Starting Django development server..."
echo "Visit http://127.0.0.1:8000/ in your browser"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver

