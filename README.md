# E-Commerce API

A fully functional e-commerce REST API built with Flask, Flask-SQLAlchemy, Flask-Marshmallow, and PostgreSQL.

## Overview

This API manages Users, Orders, and Products with proper relationships:
- **One-to-Many**: User → Orders (a user can have many orders)
- **Many-to-Many**: Order ↔ Products (an order can have multiple products, products can be in multiple orders)

## Tech Stack

- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-Marshmallow** - Serialization/deserialization
- **PostgreSQL** - Database

## Setup

### Requirements
- Python 3.11+
- PostgreSQL database (provided by Replit)

### Installation

1. Install dependencies:
```bash
pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy psycopg2-binary
```

2. Run the API:
```bash
python app.py
```

The API runs on `http://localhost:5000`

## Database Schema

### User Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(100) | Not Null |
| email | String(100) | Unique, Not Null |
| phone | String(20) | Optional |
| created_at | DateTime | Auto-generated |

### Product Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(100) | Not Null |
| description | Text | Optional |
| price | Float | Not Null |
| stock | Integer | Default: 0 |
| created_at | DateTime | Auto-generated |

### Order Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| status | String(20) | Default: 'pending' |
| total_amount | Float | Calculated |
| created_at | DateTime | Auto-generated |

### Order Items Table (Many-to-Many Association)
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| order_id | Integer | Foreign Key (orders.id) |
| product_id | Integer | Foreign Key (products.id) |
| quantity | Integer | Default: 1 |
| price_at_purchase | Float | Not Null |

## API Endpoints

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | Get all users |
| GET | `/users/<id>` | Get user by ID |
| POST | `/users` | Create a new user |
| PUT | `/users/<id>` | Update a user |
| DELETE | `/users/<id>` | Delete a user |
| GET | `/users/<id>/orders` | Get user's orders |

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Get all products |
| GET | `/products/<id>` | Get product by ID |
| POST | `/products` | Create a new product |
| PUT | `/products/<id>` | Update a product |
| DELETE | `/products/<id>` | Delete a product |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/orders` | Get all orders |
| GET | `/orders/<id>` | Get order by ID |
| POST | `/orders` | Create a new order |
| PUT | `/orders/<id>` | Update order status |
| DELETE | `/orders/<id>` | Delete an order |

## Example Requests

### Create a User
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com", "phone": "555-1234"}'
```

### Create a Product
```bash
curl -X POST http://localhost:5000/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "description": "High-performance laptop", "price": 999.99, "stock": 50}'
```

### Create an Order (with multiple products)
```bash
curl -X POST http://localhost:5000/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ]
  }'
```

### Update Order Status
```bash
curl -X PUT http://localhost:5000/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "shipped"}'
```

## Sample Response

### Order Response
```json
{
  "id": 1,
  "status": "shipped",
  "total_amount": 2149.97,
  "created_at": "2026-02-02T17:24:48",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "order_items": [
    {
      "quantity": 2,
      "price_at_purchase": 999.99,
      "product": {
        "id": 1,
        "name": "Laptop",
        "price": 999.99
      }
    }
  ]
}
```

## Files

- `app.py` - Flask API with models, schemas, and endpoints
- `main.py` - Original SQLAlchemy learning script (SQLite)

## Features

- Full CRUD operations for Users, Products, and Orders
- Marshmallow serialization for clean JSON responses
- Automatic total calculation for orders
- Price history preservation (price_at_purchase)
- Cascade deletion (deleting a user removes their orders)
- Input validation and error handling
