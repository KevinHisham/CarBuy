import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime

DATABASE = 'cars.db'

def init_db():
    """Initialize the database with cars table"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                year INTEGER NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                image_url TEXT,
                category TEXT NOT NULL,
                transmission TEXT NOT NULL,
                fuel_type TEXT NOT NULL,
                mileage INTEGER,
                color TEXT NOT NULL,
                is_available BOOLEAN DEFAULT 1,
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

def get_all_cars(filter_params=None):
    """Get all cars with optional filtering"""
    query = 'SELECT * FROM cars'
    params = []
    conditions = []
    
    if filter_params:
        if filter_params.get('brand'):
            conditions.append('brand LIKE ?')
            params.append(f"%{filter_params['brand']}%")
        
        if filter_params.get('category'):
            conditions.append('category = ?')
            params.append(filter_params['category'])
        
        if filter_params.get('minPrice'):
            conditions.append('price >= ?')
            params.append(filter_params['minPrice'])
        
        if filter_params.get('maxPrice'):
            conditions.append('price <= ?')
            params.append(filter_params['maxPrice'])
        
        if filter_params.get('transmission'):
            conditions.append('transmission = ?')
            params.append(filter_params['transmission'])
        
        if filter_params.get('fuelType'):
            conditions.append('fuel_type = ?')
            params.append(filter_params['fuelType'])
        
        if filter_params.get('isAvailable') is not None:
            conditions.append('is_available = ?')
            params.append(filter_params['isAvailable'])
    
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)
    
    query += ' ORDER BY created_at DESC'
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

def get_car_by_id(car_id):
    """Get car by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE id = ?', (car_id,))
        return cursor.fetchone()

def get_cars_by_category(category):
    """Get cars by category"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cars WHERE category = ? ORDER BY created_at DESC', (category,))
        return cursor.fetchall()

def search_cars(query):
    """Search cars by brand, model, or description"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM cars 
            WHERE brand LIKE ? OR model LIKE ? OR description LIKE ?
            ORDER BY created_at DESC
        ''', (f"%{query}%", f"%{query}%", f"%{query}%"))
        return cursor.fetchall()

def create_car(**kwargs):
    """Create a new car"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO cars (brand, model, year, price, description, image_url, 
                            category, transmission, fuel_type, mileage, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            kwargs['brand'], kwargs['model'], kwargs['year'], kwargs['price'],
            kwargs.get('description'), kwargs.get('imageUrl'), kwargs['category'],
            kwargs['transmission'], kwargs['fuelType'], kwargs.get('mileage'),
            kwargs['color']
        ))
        conn.commit()
        return get_car_by_id(cursor.lastrowid)

def update_car(car_id, **kwargs):
    """Update car"""
    fields = []
    values = []
    
    field_mapping = {
        'brand': 'brand',
        'model': 'model',
        'year': 'year',
        'price': 'price',
        'description': 'description',
        'imageUrl': 'image_url',
        'category': 'category',
        'transmission': 'transmission',
        'fuelType': 'fuel_type',
        'mileage': 'mileage',
        'color': 'color',
        'isAvailable': 'is_available'
    }
    
    for key, value in kwargs.items():
        if value is not None and key in field_mapping:
            fields.append(f"{field_mapping[key]} = ?")
            values.append(value)
    
    if not fields:
        return get_car_by_id(car_id)
    
    fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(car_id)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE cars SET {', '.join(fields)}
            WHERE id = ?
        ''', values)
        conn.commit()
        return get_car_by_id(car_id)

def delete_car(car_id):
    """Delete car"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cars WHERE id = ?', (car_id,))
        conn.commit()
        return cursor.rowcount > 0

def toggle_car_availability(car_id):
    """Toggle car availability"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE cars SET is_available = NOT is_available, updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), car_id))
        conn.commit()
        return get_car_by_id(car_id)