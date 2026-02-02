import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer, default=1)
)

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan')

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    total_amount = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', back_populates='orders')
    products = db.relationship('Product', secondary=order_items, backref='orders')

class OrderItem(db.Model):
    __tablename__ = 'order_item_details'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    price_at_purchase = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', backref='order_items')
    product = db.relationship('Product')

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        include_relationships = True

class OrderItemSchema(ma.SQLAlchemyAutoSchema):
    product = ma.Nested(ProductSchema)
    
    class Meta:
        model = OrderItem
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    user = ma.Nested(UserSchema, exclude=['orders'])
    order_items = ma.Nested(OrderItemSchema, many=True)
    
    class Meta:
        model = Order
        load_instance = True
        include_relationships = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

@app.route('/')
def home():
    return jsonify({
        'message': 'E-Commerce API',
        'endpoints': {
            'users': '/users',
            'products': '/products',
            'orders': '/orders'
        }
    })

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    
    db.session.commit()
    return jsonify(user_schema.dump(user))

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {id} deleted successfully'})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify(products_schema.dump(products))

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product_schema.dump(product))

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock=data.get('stock', 0)
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product_schema.dump(product)), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    
    db.session.commit()
    return jsonify(product_schema.dump(product))

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': f'Product {id} deleted successfully'})

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify(orders_schema.dump(orders))

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order_schema.dump(order))

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    user = User.query.get_or_404(data['user_id'])
    
    order = Order(
        user_id=user.id,
        status=data.get('status', 'pending')
    )
    db.session.add(order)
    db.session.flush()
    
    total = 0.0
    for item in data.get('items', []):
        product = Product.query.get_or_404(item['product_id'])
        quantity = item.get('quantity', 1)
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            price_at_purchase=product.price
        )
        db.session.add(order_item)
        
        order.products.append(product)
        total += product.price * quantity
    
    order.total_amount = total
    db.session.commit()
    
    return jsonify(order_schema.dump(order)), 201

@app.route('/orders/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    
    order.status = data.get('status', order.status)
    
    db.session.commit()
    return jsonify(order_schema.dump(order))

@app.route('/orders/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    
    OrderItem.query.filter_by(order_id=id).delete()
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': f'Order {id} deleted successfully'})

@app.route('/users/<int:id>/orders', methods=['GET'])
def get_user_orders(id):
    user = User.query.get_or_404(id)
    return jsonify(orders_schema.dump(user.orders))

with app.app_context():
    db.create_all()
    print("Database tables created successfully!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
