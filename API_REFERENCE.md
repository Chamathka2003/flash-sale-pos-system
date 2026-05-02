# API Reference

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. Get Products List
**GET** `/products/`

Returns all available products with current stock levels.

**Response:**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "price": "999.99",
    "stock": 50,
    "created_at": "2026-05-02T10:00:00Z",
    "updated_at": "2026-05-02T12:00:00Z"
  },
  {
    "id": 2,
    "name": "Mouse",
    "price": "29.99",
    "stock": 200,
    "created_at": "2026-05-02T10:00:00Z",
    "updated_at": "2026-05-02T12:00:00Z"
  }
]
```

---

### 2. Purchase Item (Challenge 01)
**POST** `/purchase/`

Process a single item purchase with concurrency-safe stock deduction.

**Request:**
```json
{
  "product_id": 1,
  "quantity": 1
}
```

**Response (Success - 200):**
```json
{
  "message": "Purchase successful",
  "transaction_id": 123,
  "product_id": 1,
  "quantity": 1,
  "amount": "999.99",
  "remaining_stock": 49
}
```

**Response (Insufficient Stock - 409):**
```json
{
  "error": "Insufficient stock. Available: 5",
  "available_stock": 5
}
```

**Response (Not Found - 404):**
```json
{
  "error": "Product not found"
}
```

**Response (Bad Request - 400):**
```json
{
  "error": "product_id is required"
}
```

---

### 3. Analytics Dashboard (Challenge 02)
**GET** `/analytics/`

Get daily revenue for 30 days and top 5 products by revenue.

**Query Parameters:** None

**Response:**
```json
{
  "daily_revenue": [
    {
      "date": "2026-04-02",
      "revenue": 15243.50
    },
    {
      "date": "2026-04-03",
      "revenue": 18921.75
    },
    {
      "date": "2026-04-04",
      "revenue": 12654.30
    }
  ],
  "top_products": [
    {
      "product_id": 1,
      "product_name": "Laptop",
      "revenue": 45000.00,
      "quantity_sold": 45
    },
    {
      "product_id": 3,
      "product_name": "Monitor",
      "revenue": 8999.70,
      "quantity_sold": 30
    },
    {
      "product_id": 2,
      "product_name": "Keyboard",
      "revenue": 7199.28,
      "quantity_sold": 120
    },
    {
      "product_id": 5,
      "product_name": "USB Cable",
      "revenue": 4995.00,
      "quantity_sold": 500
    },
    {
      "product_id": 4,
      "product_name": "Mouse",
      "revenue": 3599.64,
      "quantity_sold": 120
    }
  ],
  "period": "2026-03-03 to 2026-05-02"
}
```

**Performance:** <500ms (typically <100ms)

---

### 4. Checkout (Challenge 03)
**POST** `/checkout/`

Process entire shopping cart with atomic transaction guarantee.

**Request:**
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 1,
      "unit_price": 999.99
    },
    {
      "product_id": 2,
      "quantity": 2,
      "unit_price": 29.99
    },
    {
      "product_id": 3,
      "quantity": 1,
      "unit_price": 299.99
    }
  ],
  "total_amount": 1359.96
}
```

**Response (Success - 201):**
```json
{
  "message": "Checkout successful",
  "order_id": 15,
  "order_number": "ORD-ABC12345",
  "total_amount": 1359.96,
  "items_count": 3,
  "status": "completed"
}
```

**Response (Insufficient Stock - 400):**
```json
{
  "error": "Insufficient stock for Monitor. Available: 5"
}
```

**Response (Empty Cart - 400):**
```json
{
  "error": "Cart is empty"
}
```

**Response (Product Not Found - 404):**
```json
{
  "error": "Product not found"
}
```

**Important:** If ANY item fails stock check, the ENTIRE order is rolled back and nothing is saved.

---

## HTTP Status Codes

| Code | Meaning | Scenarios |
|------|---------|-----------|
| 200 | OK | Successful purchase or analytics query |
| 201 | Created | Order successfully created |
| 400 | Bad Request | Invalid input, empty cart, or checkout failure |
| 404 | Not Found | Product doesn't exist |
| 409 | Conflict | Insufficient stock for purchase |
| 500 | Server Error | Unexpected server error |

---

## Error Handling

All error responses follow this format:
```json
{
  "error": "Human-readable error message"
}
```

**Common Errors:**

1. **Missing Required Field**
   - Status: 400
   - Message: "product_id is required"

2. **Invalid Product**
   - Status: 404
   - Message: "Product not found"

3. **Out of Stock**
   - Status: 409
   - Message: "Insufficient stock. Available: X"

4. **Checkout Failure**
   - Status: 400
   - Message: "Insufficient stock for [Product Name]. Available: X"
   - Action: Entire order is rolled back

---

## CORS Configuration

The API accepts requests from:
- `http://localhost:3000` (React development server)
- `http://127.0.0.1:3000`

Add additional origins in `backend/config/settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://yourdomain.com",
]
```

---

## Rate Limiting

Currently unlimited. For production, consider:
- Django-ratelimit
- DRF throttling
- Redis-backed rate limiting

---

## Authentication

Currently no authentication (AllowAny). For production:
```python
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    # Only authenticated users
    pass
```

---

## Example cURL Commands

### Get Products
```bash
curl -X GET http://localhost:8000/api/products/
```

### Purchase Item
```bash
curl -X POST http://localhost:8000/api/purchase/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 1
  }'
```

### Get Analytics
```bash
curl -X GET http://localhost:8000/api/analytics/
```

### Checkout
```bash
curl -X POST http://localhost:8000/api/checkout/ \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 1,
        "unit_price": 999.99
      }
    ],
    "total_amount": 999.99
  }'
```

---

## Response Times

| Endpoint | Time |
|----------|------|
| `/products/` | <20ms |
| `/purchase/` | 10-50ms (with locking) |
| `/analytics/` | <100ms |
| `/checkout/` | 50-200ms (depends on cart size) |

---

## Database Schema

### Products
```
id: Integer (Primary Key)
name: String(255)
price: Decimal(10,2)
stock: Integer
created_at: DateTime
updated_at: DateTime
```

### Transactions
```
id: Integer (Primary Key)
product_id: Integer (Foreign Key → Products)
quantity: Integer
amount: Decimal(10,2)
timestamp: DateTime
date: Date (Indexed)
```

### Orders
```
id: Integer (Primary Key)
order_number: String(50) (Unique)
total_amount: Decimal(10,2)
status: String(20) [pending|completed|cancelled]
created_at: DateTime
updated_at: DateTime
```

### OrderItems
```
id: Integer (Primary Key)
order_id: Integer (Foreign Key → Orders)
product_id: Integer (Foreign Key → Products)
quantity: Integer
unit_price: Decimal(10,2)
subtotal: Decimal(10,2)
created_at: DateTime
```

---

## Pagination

For list endpoints, default pagination:
- Page size: 100 items
- Add `?page=2` to get next page
- Response includes pagination info

---

## Testing with Postman

1. Import this collection into Postman
2. Set base URL: `{{BASE_URL}}`
3. Set in Postman variables:
   - `BASE_URL` = `http://localhost:8000/api`
   - `product_id` = `1`
   - `total_amount` = `1359.96`

**Sample Postman Environment:**
```json
{
  "name": "Flash Sale POS",
  "values": [
    {"key": "BASE_URL", "value": "http://localhost:8000/api", "enabled": true},
    {"key": "product_id", "value": "1", "enabled": true},
    {"key": "order_id", "value": "15", "enabled": true}
  ]
}
```

---

## Troubleshooting

### "Connection refused"
- Ensure Django server is running: `python manage.py runserver`
- Check port: Should be `localhost:8000`

### "CORS error"
- Frontend must be on allowed origin
- Check `settings.py` CORS_ALLOWED_ORIGINS
- Add frontend URL if missing

### "Product not found"
- Create products first or populate data: `python populate_data.py`
- Or use admin panel: `http://localhost:8000/admin/`

### "Insufficient stock"
- This is expected! Stock is limited by design
- Try with a different product or wait for restock

### "Request timeout"
- Analytics endpoint can take 100-500ms with large datasets
- Ensure MySQL is responsive: `mysql -u root -p -e "SELECT 1;"`
