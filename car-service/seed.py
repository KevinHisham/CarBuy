from database import get_all_cars, create_car

def seed_data():
    """Seed initial data if database is empty"""
    cars = get_all_cars()
    
    if len(cars) == 0:
        print("Seeding car data...")
        
        sample_cars = [
            {
                "brand": "Toyota",
                "model": "Avanza",
                "year": 2022,
                "price": 230000000.0,
                "description": "MPV 7 seater yang nyaman untuk keluarga",
                "imageUrl": "https://i.imgur.com/wkz8JRy.jpg",
                "category": "MPV",
                "transmission": "Manual",
                "fuelType": "Gasoline",
                "mileage": 15000,
                "color": "White"
            },
            {
                "brand": "Honda",
                "model": "Civic",
                "year": 2023,
                "price": 580000000.0,
                "description": "Sedan sporty dengan performa tinggi",
                "imageUrl": "https://i.imgur.com/XEGEMn1.jpg",
                "category": "Sedan",
                "transmission": "CVT",
                "fuelType": "Gasoline",
                "mileage": 8000,
                "color": "Black"
            },
            {
                "brand": "Mitsubishi",
                "model": "Pajero Sport",
                "year": 2021,
                "price": 520000000.0,
                "description": "SUV tangguh untuk berbagai medan",
                "imageUrl": "https://i.imgur.com/00AXHsa.jpg",
                "category": "SUV",
                "transmission": "Automatic",
                "fuelType": "Diesel",
                "mileage": 25000,
                "color": "Silver"
            },
            {
                "brand": "Daihatsu",
                "model": "Ayla",
                "year": 2020,
                "price": 140000000.0,
                "description": "Hatchback ekonomis dan irit bahan bakar",
                "imageUrl": "https://i.imgur.com/HaOchWt.jpg",
                "category": "Hatchback",
                "transmission": "Manual",
                "fuelType": "Gasoline",
                "mileage": 35000,
                "color": "Red"
            },
            {
                "brand": "Suzuki",
                "model": "Ertiga",
                "year": 2022,
                "price": 250000000.0,
                "description": "MPV compact dengan fitur lengkap",
                "imageUrl": "https://i.imgur.com/MG3CcWn.jpg",
                "category": "MPV",
                "transmission": "Automatic",
                "fuelType": "Gasoline",
                "mileage": 12000,
                "color": "Blue"
            }
        ]
        
        for car_data in sample_cars:
            create_car(**car_data)
        
        print(f"Seeded {len(sample_cars)} cars")
    else:
        print(f"Database already has {len(cars)} cars")