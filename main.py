from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    
    orders = relationship('Order', back_populates='product')
    
    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    status = Column(Boolean, default=False)
    
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')
    
    def __repr__(self):
        return f"Order(id={self.id}, user_id={self.user_id}, product_id={self.product_id}, quantity={self.quantity}, shipped={self.status})"

Base.metadata.create_all(engine)

print("=" * 60)
print("PART 4: INSERTING DATA")
print("=" * 60)

user1 = User(name='Alice Johnson', email='alice@example.com')
user2 = User(name='Bob Smith', email='bob@example.com')
user3 = User(name='Charlie Brown', email='charlie@example.com')

session.add_all([user1, user2, user3])
session.commit()
print("Added 3 users")

product1 = Product(name='Laptop', price=999)
product2 = Product(name='Headphones', price=149)
product3 = Product(name='Keyboard', price=79)

session.add_all([product1, product2, product3])
session.commit()
print("Added 3 products")

order1 = Order(user_id=user1.id, product_id=product1.id, quantity=1, status=True)
order2 = Order(user_id=user1.id, product_id=product2.id, quantity=2, status=False)
order3 = Order(user_id=user2.id, product_id=product3.id, quantity=3, status=True)
order4 = Order(user_id=user2.id, product_id=product1.id, quantity=1, status=False)
order5 = Order(user_id=user3.id, product_id=product2.id, quantity=1, status=False)

session.add_all([order1, order2, order3, order4, order5])
session.commit()
print("Added 5 orders")

print("\n" + "=" * 60)
print("PART 5: QUERIES")
print("=" * 60)

print("\n--- All Users ---")
users = session.query(User).all()
for user in users:
    print(f"  ID: {user.id}, Name: {user.name}, Email: {user.email}")

print("\n--- All Products ---")
products = session.query(Product).all()
for product in products:
    print(f"  Name: {product.name}, Price: ${product.price}")

print("\n--- All Orders (with User and Product details) ---")
orders = session.query(Order).all()
for order in orders:
    print(f"  User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}, Shipped: {'Yes' if order.status else 'No'}")

print("\n--- Updating Product Price ---")
laptop = session.query(Product).filter_by(name='Laptop').first()
print(f"  Before: {laptop.name} - ${laptop.price}")
laptop.price = 899
session.commit()
print(f"  After: {laptop.name} - ${laptop.price}")

print("\n--- Deleting User by ID ---")
user_to_delete = session.query(User).filter_by(id=user3.id).first()
if user_to_delete:
    print(f"  Deleting user: {user_to_delete.name}")
    session.delete(user_to_delete)
    session.commit()
    print("  User deleted successfully")

print("\n" + "=" * 60)
print("PART 6: BONUS FEATURES")
print("=" * 60)

print("\n--- Orders Not Shipped ---")
unshipped_orders = session.query(Order).filter_by(status=False).all()
for order in unshipped_orders:
    print(f"  Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}")

print("\n--- Total Orders Per User ---")
order_counts = session.query(User.name, func.count(Order.id).label('total_orders')).join(Order).group_by(User.id).all()
for user_name, total in order_counts:
    print(f"  {user_name}: {total} order(s)")

print("\n" + "=" * 60)
print("VERIFICATION: Remaining Users and Orders")
print("=" * 60)

print("\n--- Remaining Users ---")
remaining_users = session.query(User).all()
for user in remaining_users:
    print(f"  {user}")

print("\n--- Remaining Orders ---")
remaining_orders = session.query(Order).all()
for order in remaining_orders:
    print(f"  {order}")

session.close()
print("\nDatabase operations completed successfully!")
