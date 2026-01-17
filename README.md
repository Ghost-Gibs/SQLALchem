# SQLAlchemy Shop Database

A Python project demonstrating relational database management using SQLAlchemy ORM with SQLite.

## Overview

This project creates and manages a shop database with three related tables:
- **Users** - Customer information
- **Products** - Available products with prices
- **Orders** - Links users to products with quantities and shipping status

## Setup

### Requirements
- Python 3.11+
- SQLAlchemy

### Installation

1. Install dependencies:
```bash
pip install sqlalchemy
```

2. Run the script:
```bash
python main.py
```

## Database Schema

### User Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String | - |
| email | String | Unique |

### Product Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String | - |
| price | Integer | - |

### Order Table
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| user_id | Integer | Foreign Key (users.id) |
| product_id | Integer | Foreign Key (products.id) |
| quantity | Integer | - |
| status | Boolean | Default: False (shipped status) |

## Relationships

- A **User** can have many **Orders** (one-to-many)
- A **Product** can appear in many **Orders** (one-to-many)
- When a User is deleted, their Orders are automatically deleted (cascade)

## Features Demonstrated

### CRUD Operations
- **Create**: Add users, products, and orders
- **Read**: Query all users, products, and orders with relationships
- **Update**: Modify product prices
- **Delete**: Remove users by ID (with cascade deletion of orders)

### Queries
- Retrieve all users with their information
- List all products with names and prices
- Display orders with user names, product names, and quantities
- Find all unshipped orders (status = False)
- Count total orders per user

## Usage

Run the script to:
1. Create the SQLite database (`shop.db`)
2. Insert sample data (3 users, 3 products, 5 orders)
3. Execute and display query results
4. Demonstrate update and delete operations

### Re-running the Script

If you run the script multiple times, delete the existing database first:
```bash
rm shop.db
python main.py
```

## Sample Output

```
PART 4: INSERTING DATA
Added 3 users
Added 3 products
Added 5 orders

PART 5: QUERIES
--- All Users ---
  ID: 1, Name: Alice Johnson, Email: alice@example.com
  ID: 2, Name: Bob Smith, Email: bob@example.com
  ...

--- All Orders (with User and Product details) ---
  User: Alice Johnson, Product: Laptop, Quantity: 1, Shipped: Yes
  ...
```

## Files

- `main.py` - Main script with all database operations
- `shop.db` - SQLite database (created when script runs)
