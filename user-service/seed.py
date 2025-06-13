from database import get_all_users, create_user

def seed_data():
    """Seed initial data if database is empty"""
    users = get_all_users()
    
    if len(users) == 0:
        print("Seeding user data...")
        
        sample_users = [
            {
                "name": "John Doe",
                "email": "john.doe@example.com",
                "phone": "+62812345678",
                "address": "Jl. Sudirman No. 123, Jakarta"
            },
            {
                "name": "Jane Smith",
                "email": "jane.smith@example.com",
                "phone": "+62887654321",
                "address": "Jl. Thamrin No. 456, Jakarta"
            },
            {
                "name": "Ahmad Rahman",
                "email": "ahmad.rahman@example.com",
                "phone": "+62811223344",
                "address": "Jl. Asia Afrika No. 789, Bandung"
            }
        ]
        
        for user_data in sample_users:
            create_user(**user_data)
        
        print(f"Seeded {len(sample_users)} users")
    else:
        print(f"Database already has {len(users)} users")