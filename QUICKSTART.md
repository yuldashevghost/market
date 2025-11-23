# Quick Start Guide

## Prerequisites Installation

First, install the required system packages:

```bash
sudo apt install python3-venv python3-pip
```

## Setup (One-time)

Run the setup script:

```bash
./setup.sh
```

Or manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Load sample data (optional)
python manage.py load_sample_data
```

## Running the Project

After setup, to run the development server:

```bash
# Activate virtual environment (if not already activated)
source venv/bin/activate

# Run the server
python manage.py runserver
```

Then visit:
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Troubleshooting

If you get "ModuleNotFoundError: No module named 'django'":
- Make sure the virtual environment is activated: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r requirements.txt`

