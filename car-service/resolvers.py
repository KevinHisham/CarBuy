from ariadne import QueryType, MutationType
from database import (
    get_all_cars, get_car_by_id, get_cars_by_category, search_cars,
    create_car, update_car, delete_car, toggle_car_availability
)

query = QueryType()
mutation = MutationType()

def car_to_dict(car_row):
    """Convert database row to dictionary"""
    if not car_row:
        return None
    
    return {
        "id": str(car_row["id"]),
        "brand": car_row["brand"],
        "model": car_row["model"],
        "year": car_row["year"],
        "price": float(car_row["price"]),
        "description": car_row["description"],
        "imageUrl": car_row["image_url"],
        "category": car_row["category"],
        "transmission": car_row["transmission"],
        "fuelType": car_row["fuel_type"],
        "mileage": car_row["mileage"],
        "color": car_row["color"],
        "isAvailable": bool(car_row["is_available"]),
        "createdAt": car_row["created_at"],
        "updatedAt": car_row["updated_at"]
    }

@query.field("cars")
def resolve_cars(_, info, filter=None):
    cars = get_all_cars(filter)
    return [car_to_dict(car) for car in cars]

@query.field("car")
def resolve_car(_, info, id):
    car = get_car_by_id(int(id))
    return car_to_dict(car)

@query.field("availableCars")
def resolve_available_cars(*_):
    cars = get_all_cars({'isAvailable': True})
    return [car_to_dict(car) for car in cars]

@query.field("carsByCategory")
def resolve_cars_by_category(_, info, category):
    cars = get_cars_by_category(category)
    return [car_to_dict(car) for car in cars]

@query.field("searchCars")
def resolve_search_cars(_, info, query):
    cars = search_cars(query)
    return [car_to_dict(car) for car in cars]

@mutation.field("createCar")
def resolve_create_car(_, info, input):
    try:
        car = create_car(**input)
        return car_to_dict(car)
    except Exception as e:
        raise Exception(f"Failed to create car: {str(e)}")

@mutation.field("updateCar")
def resolve_update_car(_, info, id, input):
    try:
        car = update_car(int(id), **input)
        if not car:
            raise Exception("Car not found")
        return car_to_dict(car)
    except Exception as e:
        raise Exception(f"Failed to update car: {str(e)}")

@mutation.field("deleteCar")
def resolve_delete_car(_, info, id):
    try:
        return delete_car(int(id))
    except Exception as e:
        raise Exception(f"Failed to delete car: {str(e)}")

@mutation.field("toggleCarAvailability")
def resolve_toggle_car_availability(_, info, id):
    try:
        car = toggle_car_availability(int(id))
        if not car:
            raise Exception("Car not found")
        return car_to_dict(car)
    except Exception as e:
        raise Exception(f"Failed to toggle car availability: {str(e)}")