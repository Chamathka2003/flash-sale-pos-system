# Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.9+
- Node.js 16+
- MySQL 5.7+

### Windows Users
```bash
# Run setup script
setup.bat
```

### macOS/Linux Users
```bash
# Run setup script
chmod +x setup.sh
./setup.sh
```

### Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE assignment_db;"
python manage.py migrate
python manage.py runserver
```

**Frontend (in new terminal):**
```bash
cd frontend
npm install
npm start
```

## Usage

1. Open http://localhost:3000
2. Browse products
3. Add to cart and checkout
4. View receipt

## Run Tests

```bash
# Terminal 1: Backend server
cd backend
python manage.py runserver

# Terminal 2: Load test
cd backend
python load_test.py

# Terminal 3: Data population
cd backend
python populate_data.py
```

## Endpoints

- `/api/products/` - Get all products
- `/api/purchase/` - Buy item (POST)
- `/api/checkout/` - Checkout cart (POST)
- `/api/analytics/` - Get analytics (GET)
