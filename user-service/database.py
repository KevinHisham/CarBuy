import sqlite3
import os
from contextlib import contextmanager
from datetime import datetime

DATABASE = 'users.db'

def init_db():
    """Initialize the database with users table"""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                address TEXT,
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

def get_all_users():
    """Get all users"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        return cursor.fetchall()

def get_user_by_id(user_id):
    """Get user by ID"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()

def get_user_by_email(email):
    """Get user by email"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()

def create_user(name, email, phone=None, address=None):
    """Create a new user"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, address))
        conn.commit()
        return get_user_by_id(cursor.lastrowid)

def update_user(user_id, **kwargs):
    """Update user"""
    fields = []
    values = []
    
    for key, value in kwargs.items():
        if value is not None:
            fields.append(f"{key} = ?")
            values.append(value)
    
    if not fields:
        return get_user_by_id(user_id)
    
    fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(user_id)
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(f'''
            UPDATE users SET {', '.join(fields)}
            WHERE id = ?
        ''', values)
        conn.commit()
        return get_user_by_id(user_id)

def delete_user(user_id):
    """Delete user"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        return cursor.rowcount > 0