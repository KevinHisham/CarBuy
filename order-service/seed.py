from database import get_all_orders, create_order

def seed_data():
    """Seed initial data if database is empty"""
    orders = get_all_orders()
    
    if len(orders) == 0:
        print("Seeding order data...")
        
        sample_orders = [
            {
                "user_id": 1,
                "car_id": 1,
                "total_amount": 230000000.0,
                "payment_method": "Bank Transfer",
                "notes": "Mohon disiapkan untuk pengambilan hari Senin"
            },
            {
                "user_id": 2,
                "car_id": 2,
                "total_amount": 580000000.0,
                "payment_method": "Credit Card",
                "notes": "Pembayaran akan dilakukan secara kredit"
            },
            {
                "user_id": 3,
                "car_id": 3,
                "total_amount": 520000000.0,
                "payment_method": "Cash",
                "notes": "Pembayaran tunai langsung saat pengambilan"
            }
        ]
        
        for order_data in sample_orders:
            create_order(**order_data)
        
        print(f"Seeded {len(sample_orders)} orders")
    else:
        print(f"Database already has {len(orders)} orders")