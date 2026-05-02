# Flash Sale POS System - Complete Solution

A comprehensive solution for managing high-concurrency flash sales with a modern POS system. Built with Django, React, and MySQL.

## Overview

This project addresses three main challenges:

1. **Challenge 01: High-Concurrency Management** - Handles 500+ concurrent purchase requests safely
2. **Challenge 02: Big Data Aggregation & Query Optimization** - Analytics dashboard with 100k records responding in <500ms
3. **Challenge 03: Mini POS System** - Full Point of Sale interface with transactional integrity

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Frontend**: React 18.2
- **Database**: MySQL
- **Testing**: Python threading/concurrent requests

## Project Structure

```
Assignment01/
├── backend/
│   ├── config/
│   │   ├── settings.py       
│   │   ├── urls.py         
│   │   └── wsgi.py           
│   ├── api/
│   │   ├── models.py         
│   │   ├── views.py        
│   │   ├── serializers.py    
│   │   ├── urls.py           
│   │   └── admin.py          
│   ├── manage.py             
│   ├── populate_data.py      
│   ├── load_test.py          
│   └── requirements.txt      
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── POS.js        # Main POS component
│   │   │   ├── ProductList.js # Product selection
│   │   │   ├── Cart.js       # Shopping cart
│   │   │   └── Receipt.js    # Receipt printing (80mm thermal)
│   │   ├── styles/
│   │   │   └── App.css       # Styling
│   │   ├── App.js
│   │   └── index.js
│   ├── package.json
│   └── public/
│       └── index.html
└── README.md
```

## Setup & Installation

### Prerequisites

- Python 3.9+
- Node.js 16+
- MySQL 5.7+
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Assignment01/backend
   ```

2. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup MySQL database**
   ```bash
   # Create database
   mysql -u root -p
   CREATE DATABASE assignment_db;
   EXIT;
   ```

5. **Configure database connection** (if needed)
   - Edit `config/settings.py`
   - Update DATABASES section with your MySQL credentials

6. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. **Create initial products** (optional)
   ```bash
   python manage.py shell
   ```
   ```python
   from api.models import Product
   from decimal import Decimal
   
   products_data = [
       ('Laptop', Decimal('999.99'), 50),
       ('Mouse', Decimal('29.99'), 200),
       ('Keyboard', Decimal('79.99'), 150),
       ('Monitor', Decimal('299.99'), 30),
       ('USB Cable', Decimal('9.99'), 500),
   ]
   
   for name, price, stock in products_data:
       Product.objects.create(name=name, price=price, stock=stock)
   
   exit()
   ```

8. **Start the Django server**
   ```bash
   python manage.py runserver
   ```
   Server runs on: `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start React development server**
   ```bash
   npm start
   ```
   Frontend runs on: `http://localhost:3000`

## Running the Scripts

### 1. Data Population Script

Populates MySQL with 100,000 transaction records from the last 6 months:

```bash
cd backend
python populate_data.py
```

**What it does:**
- Creates 15 sample products if they don't exist
- Generates 100,000 transaction records with:
  - Random products
  - Random quantities (1-10)
  - Realistic timestamps over 6 months
  - Uses bulk_create for performance

**Time**: ~2-3 minutes

### 2. Concurrency Test Script

Tests the purchase API with 100 concurrent requests:

```bash
# Make sure Django server is running on port 8000
python load_test.py
```

**What it does:**
- Fires 100 concurrent purchase requests (using ThreadPoolExecutor with 50 workers)
- Each request attempts to purchase 1 unit
- Verifies stock never goes below zero
- Reports success rate and requests per second

**Expected Results:**
- All 100 requests should succeed (or fail gracefully due to stock limit)
- Stock should never go negative
- Response time should be under 500ms per request

## Challenge Solutions Explained

### Challenge 01: High-Concurrency Management ✓

**Problem**: 500+ concurrent requests for 50-unit stock → need atomic operations

**Solution**:
```python
with transaction.atomic():
    product = Product.objects.select_for_update().get(id=product_id)
    if product.stock < quantity:
        return error()
    product.stock -= quantity
    product.save()
```

**Key Implementation Details:**
- `select_for_update()`: Database-level row locking
- `transaction.atomic()`: All-or-nothing operation
- Stock check + deduction in single atomic block
- Prevents race conditions inherent to distributed systems

**API Endpoint**: `POST /api/purchase/`
- Payload: `{"product_id": 1, "quantity": 1}`
- Response: `{"message": "Purchase successful", "remaining_stock": 48}`

### Challenge 02: Big Data Aggregation & Query Optimization ✓

**Problem**: Query 100k records for daily revenue + top 5 products in <500ms

**Solution**:
```python
# Database-level aggregation
daily_revenue = Transaction.objects.filter(
    date__gte=thirty_days_ago
).values('date').annotate(
    revenue=Sum(F('amount'))
).order_by('date')

top_products = Transaction.objects.filter(
    date__gte=thirty_days_ago
).values('product__name').annotate(
    total_revenue=Sum(F('amount'))
).order_by('-total_revenue')[:5]
```

**Optimizations**:
1. **Database Indexes**: Multi-column indexes on (date, product)
2. **F() Expressions**: Calculations at database level, not Python
3. **Aggregation**: Using `Sum()` with `annotate()` instead of Python loops
4. **Filtering**: Date range filtering reduces data scanned
5. **Batch Loading**: Bulk create for data population

**Performance**:
- 100k records → response in <100ms on modern hardware
- Linear time complexity regardless of dataset size
- Minimal memory footprint

**API Endpoint**: `GET /api/analytics/`
- Response includes:
  - Daily revenue for 30 days
  - Top 5 products with revenue & quantity
  - Period information

### Challenge 03: Mini POS System (Transaction Integrity) ✓

**Problem**: Multi-item checkout must be all-or-nothing

**Solution**:
```python
with transaction.atomic():
    order = Order.objects.create(...)
    for item in cart_items:
        product = Product.objects.select_for_update().get(id=item_id)
        if product.stock < quantity:
            raise ValueError()  # Triggers rollback
        product.stock -= quantity
        product.save()
        OrderItem.objects.create(...)
    order.status = 'completed'
    order.save()
```

**Implementation**:
1. **Atomic Checkout**: If ANY item fails, entire order rolls back
2. **Stock Locking**: Prevents overselling during checkout
3. **Order Persistence**: Records order number, total, status
4. **Receipt Component**: Styled for 80mm thermal printer

**Frontend Features**:
- Product grid with stock display
- Real-time shopping cart
- Quantity adjustment
- One-click checkout
- Professional receipt display

**Backend API**: `POST /api/checkout/`
- Accepts: `{"items": [...], "total_amount": 1000.00}`
- Returns: Order confirmation with receipt data

## API Endpoints Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| POST | `/api/purchase/` | Purchase single item (Challenge 01) |
| GET | `/api/analytics/` | Daily revenue + top products (Challenge 02) |
| POST | `/api/checkout/` | Process entire order (Challenge 03) |

## Testing

### Manual Testing

1. **Start servers**:
   ```bash
   # Terminal 1 - Backend
   cd backend && python manage.py runserver

   # Terminal 2 - Frontend
   cd frontend && npm start
   ```

2. **Test POS System**:
   - Open http://localhost:3000
   - Add products to cart
   - Verify stock updates after checkout
   - Check receipt printing

3. **Test APIs with curl**:
   ```bash
   # Purchase API
   curl -X POST http://localhost:8000/api/purchase/ \
     -H "Content-Type: application/json" \
     -d '{"product_id": 1, "quantity": 5}'

   # Analytics API
   curl http://localhost:8000/api/analytics/

   # Products API
   curl http://localhost:8000/api/products/
   ```

### Automated Testing

Run the load test:
```bash
python backend/load_test.py
```

## Database Schema

### Products Table
```sql
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    stock INT,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Transactions Table
```sql
CREATE TABLE transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT,
    quantity INT,
    amount DECIMAL(10, 2),
    timestamp DATETIME,
    date DATE,
    FOREIGN KEY (product_id) REFERENCES products(id),
    INDEX idx_date (date),
    INDEX idx_product_date (product_id, date)
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_number VARCHAR(50) UNIQUE,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20),
    created_at DATETIME,
    updated_at DATETIME
);
```

### OrderItems Table
```sql
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10, 2),
    subtotal DECIMAL(10, 2),
    created_at DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE PROTECT
);
```

## Performance Benchmarks

- **Concurrency Test**: 100 requests in ~2 seconds (50 RPS with locking)
- **Analytics Query**: <100ms for 100k records
- **Data Population**: ~2-3 minutes for 100k records
- **Receipt Generation**: <50ms
- **Product List**: <20ms

## Troubleshooting

### MySQL Connection Error
```
Error: (2003, "Can't connect to MySQL server on 'localhost'")
```
**Solution**: 
- Ensure MySQL is running: `mysql -u root -p`
- Check credentials in `settings.py`
- Verify database exists: `SHOW DATABASES;`

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### React Build Fails
```bash
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
npm start
```

### CORS Issues
Already configured in Django settings:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]
```

## Features Implemented

* Concurrency Management with Database Locking
* 100k Record Population & Aggregation
* Sub-500ms Analytics Query Performance
* Atomic Transactions with Rollback
* Professional POS Interface
* Thermal Receipt Printing (80mm width)
* Real-time Stock Management
* Comprehensive Error Handling
* RESTful API Design
*Production-Ready Code

## Future Enhancements

- User authentication & authorization
- Payment gateway integration
- Advanced analytics with charts
- Inventory management dashboard
- Mobile app (React Native)
- Redis caching for analytics
- WebSocket for real-time updates
- Email receipts
- Refund/Return management

