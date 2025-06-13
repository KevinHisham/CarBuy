import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime

DATABASE = 'orders.db'

def init_db():
    """Initialize the database with orders table"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                car_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'PENDING',
                payment_status TEXT DEFAULT 'PENDING',
                payment_method TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@contextmanager
def get_db():
    """Context manager for database connections"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_all_orders():
    """Get all orders"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders ORDER BY created_at DESC')
        return cursor.fetchall()

def get_order_by_id(order_id):
    """Get order by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
        return cursor.fetchone()

def get_orders_by_user(user_id):
    """Get orders by user ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        return cursor.fetchall()

def get_orders_by_car(car_id):
    """Get orders by car ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE car_id = ? ORDER BY created_at DESC', (car_id,))
        return cursor.fetchall()

def get_orders_by_status(status):
    """Get orders by status"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC', (status,))
        return cursor.fetchall()

def get_order_stats():
    """Get order statistics"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = cursor.fetchone()[0]
        
        # Pending orders
        cursor.execute('SELECT COUNT(*) FROM orders WHERE status = ?', ('PENDING',))
        pending_orders = cursor.fetchone()[0]
        
        # Completed orders
        cursor.execute('SELECT COUNT(*) FROM orders WHERE status = ?', ('COMPLETED',))
        completed_orders = cursor.fetchone()[0]
        
        # Total revenue (from completed orders with paid status)
        cursor.execute('''
            SELECT COALESCE(SUM(total_amount), 0) 
            FROM orders 
            WHERE status = 'COMPLETED' AND payment_status = 'PAID'
        ''')
        total_revenue = cursor.fetchone()[0]
        
        return {
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'total_revenue': float(total_revenue)
        }

def create_order(user_id, car_id, total_amount, payment_method=None, notes=None):
    """Create a new order"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (user_id, car_id, total_amount, payment_method, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, car_id, total_amount, payment_method, notes))
        conn.commit()
        return get_order_by_id(cursor.lastrowid)

def update_order(order_id, **kwargs):
    """Update order"""
    fields = []
    values = []
    
    field_mapping = {
        'status': 'status',
        'paymentStatus': 'payment_status',
        'paymentMethod': 'payment_method',
        'notes': 'notes'
    }
    
    for key, value in kwargs.items():
        if value is not None and key in field_mapping:
            fields.append(f"{field_mapping[key]} = ?")
            values.append(value)
    
    if not fields:
        return get_order_by_id(order_id)
    
    fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(order_id)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE orders SET {', '.join(fields)}
            WHERE id = ?
        ''', values)
        conn.commit()
        return get_order_by_id(order_id)

def cancel_order(order_id):
    """Cancel order"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE orders SET status = 'CANCELLED', updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), order_id))
        conn.commit()
        return get_order_by_id(order_id)

def confirm_payment(order_id):
    """Confirm payment for order"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE orders SET payment_status = 'PAID', status = 'CONFIRMED', updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), order_id))
        conn.commit()
        return get_order_by_id(order_id)