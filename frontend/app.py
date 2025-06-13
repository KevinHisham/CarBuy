from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests
import os
from config import Config
from services import UserService, CarService, OrderService

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'frontend_secret_key')
app.config.from_object(Config)

# Initialize services
user_service = UserService()
car_service = CarService()
order_service = OrderService()

@app.route('/')
def index():
    """Home page"""
    try:
        cars = car_service.get_available_cars()
        featured_cars = cars[:6] if cars else []
        return render_template('index.html', featured_cars=featured_cars)
    except Exception as e:
        print(f"Error loading home page: {e}")
        return render_template('index.html', featured_cars=[])

@app.route('/cars')
def cars():
    """Cars listing page"""
    try:
        # Get filter parameters
        brand = request.args.get('brand')
        category = request.args.get('category')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Build filter
        car_filter = {}
        if brand:
            car_filter['brand'] = brand
        if category:
            car_filter['category'] = category
        if min_price:
            car_filter['minPrice'] = min_price
        if max_price:
            car_filter['maxPrice'] = max_price
        
        cars_list = car_service.get_cars(car_filter)
        return render_template('cars.html', cars=cars_list)
    except Exception as e:
        print(f"Error loading cars: {e}")
        return render_template('cars.html', cars=[])

@app.route('/car/<int:car_id>')
def car_detail(car_id):
    """Car detail page"""
    try:
        car = car_service.get_car(car_id)
        if not car:
            return "Car not found", 404
        return render_template('car_detail.html', car=car)
    except Exception as e:
        print(f"Error loading car detail: {e}")
        return "Error loading car", 500

@app.route('/cart')
def cart():
    """Shopping cart page"""
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/orders')
def orders():
    """Orders page"""
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    try:
        user_orders = order_service.get_user_orders(user_id)
        return render_template('orders.html', orders=user_orders)
    except Exception as e:
        print(f"Error loading orders: {e}")
        return render_template('orders.html', orders=[])

@app.route('/api/add_to_cart', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    try:
        data = request.get_json()
        car_id = data.get('car_id')
        quantity = data.get('quantity', 1)
        
        car = car_service.get_car(car_id)
        if not car:
            return jsonify({'success': False, 'message': 'Car not found'})
        
        cart = session.get('cart', [])
        
        # Check if car already in cart
        for item in cart:
            if item['car_id'] == car_id:
                item['quantity'] += quantity
                break
        else:
            cart.append({
                'car_id': car_id,
                'name': f"{car['brand']} {car['model']}",
                'price': car['price'],
                'quantity': quantity,
                'image': car.get('imageUrl', '')
            })
        
        session['cart'] = cart
        return jsonify({'success': True, 'message': 'Added to cart'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/remove_from_cart', methods=['POST'])
def remove_from_cart():
    """Remove item from cart"""
    try:
        data = request.get_json()
        car_id = data.get('car_id')
        
        cart = session.get('cart', [])
        cart = [item for item in cart if item['car_id'] != car_id]
        session['cart'] = cart
        
        return jsonify({'success': True, 'message': 'Removed from cart'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """Process checkout"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'Please login first'})
    
    try:
        cart = session.get('cart', [])
        if not cart:
            return jsonify({'success': False, 'message': 'Cart is empty'})
        
        # Create order
        order_data = {
            'userId': user_id,
            'items': [{'carId': item['car_id'], 'quantity': item['quantity']} for item in cart],
        }
        
        order = order_service.create_order(order_data)
        if order:
            session['cart'] = []  # Clear cart
            return jsonify({'success': True, 'message': 'Order created successfully', 'order_id': order['id']})
        else:
            return jsonify({'success': False, 'message': 'Failed to create order'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        # Simple login - in real app, you'd verify password
        try:
            user = user_service.get_user_by_email(email)
            if user:
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                return redirect(url_for('index'))
            else:
                return render_template('login.html', error='User not found')
        except Exception as e:
            return render_template('login.html', error='Login failed')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)