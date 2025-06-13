import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Service URLs - untuk production di Railway
    USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL') or 'http://localhost:8001/graphql'
    CAR_SERVICE_URL = os.environ.get('CAR_SERVICE_URL') or 'http://localhost:8002/graphql'
    ORDER_SERVICE_URL = os.environ.get('ORDER_SERVICE_URL') or 'http://localhost:8003/graphql'
    
    # CarPay integration
    CARPAY_URL = os.environ.get('CARPAY_URL') or 'http://localhost:8000/graphql'