# SQLAlchemy Shop Database

## Overview

This is a Python project demonstrating relational database management using SQLAlchemy ORM with SQLite. The application creates and manages a shop database with three related tables: Users (customer information), Products (available items with prices), and Orders (linking users to products with quantities and shipping status). The project serves as a learning exercise for understanding SQLAlchemy relationships, CRUD operations, and basic database design patterns.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### ORM Layer
- **Technology**: SQLAlchemy ORM with declarative base pattern
- **Rationale**: Provides a clean, Pythonic way to interact with databases using Python classes instead of raw SQL
- **Pattern**: Each database table is represented as a Python class inheriting from `Base`

### Database
- **Technology**: SQLite (file-based at `shop.db`)
- **Rationale**: Simple setup with no server required, ideal for learning and small applications
- **Trade-off**: Not suitable for concurrent access or production workloads, but perfect for this educational context

### Data Models
Three interconnected models following a typical e-commerce pattern:

1. **User**: Stores customer data with unique email constraint
2. **Product**: Stores item catalog with pricing
3. **Order**: Junction table linking users to products with quantity and status tracking

### Relationships
- **User → Orders**: One-to-many with cascade delete (deleting a user removes their orders)
- **Product → Orders**: One-to-many (products can appear in multiple orders)
- **Bidirectional**: Uses `back_populates` for two-way navigation between related objects

### Session Management
- Uses `sessionmaker` bound to the engine for database transactions
- Single global session instance for simplicity

## External Dependencies

### Python Packages
| Package | Purpose |
|---------|---------|
| SQLAlchemy | ORM framework for database operations |

### Database
- **SQLite**: Embedded database, no external service required
- **File Location**: `shop.db` in project root (auto-created on first run)

### Runtime Requirements
- Python 3.11+