import requests
from config import Config

class GraphQLService:
    def __init__(self, url):
        self.url = url
    
    def execute_query(self, query, variables=None):
        """Execute GraphQL query"""
        try:
            payload = {'query': query}
            if variables:
                payload['variables'] = variables
            
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if 'errors' in result:
                raise Exception(f"GraphQL errors: {result['errors']}")
            
            return result.get('data')
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except Exception as e:
            print(f"GraphQL error: {e}")
            return None

class UserService(GraphQLService):
    def __init__(self):
        super().__init__(Config.USER_SERVICE_URL)
    
    def get_user(self, user_id):
        """Get user by ID"""
        query = """
        query GetUser($id: ID!) {
            user(id: $id) {
                id
                name
                email
                phone
                address
            }
        }
        """
        result = self.execute_query(query, {'id': user_id})
        return result.get('user') if result else None
    
    def get_user_by_email(self, email):
        """Get user by email"""
        query = """
        query GetUserByEmail($email: String!) {
            userByEmail(email: $email) {
                id
                name
                email
                phone
                address
            }
        }
        """
        result = self.execute_query(query, {'email': email})
        return result.get('userByEmail') if result else None
    
    def create_user(self, user_data):
        """Create new user"""
        query = """
        mutation CreateUser($input: UserInput!) {
            createUser(input: $input) {
                id
                name
                email
                phone
                address
            }
        }
        """
        result = self.execute_query(query, {'input': user_data})
        return result.get('createUser') if result else None

class CarService(GraphQLService):
    def __init__(self):
        super().__init__(Config.CAR_SERVICE_URL)
    
    def get_cars(self, car_filter=None):
        """Get cars with optional filter"""
        query = """
        query GetCars($filter: CarFilter) {
            cars(filter: $filter) {
                id
                brand
                model
                year
                price
                description
                imageUrl
                category
                transmission
                fuelType
                mileage
                color
                isAvailable
            }
        }
        """
        variables = {'filter': car_filter} if car_filter else {}
        result = self.execute_query(query, variables)
        return result.get('cars', []) if result else []
    
    def get_car(self, car_id):
        """Get car by ID"""
        query = """
        query GetCar($id: ID!) {
            car(id: $id) {
                id
                brand
                model
                year
                price
                description
                imageUrl
                category
                transmission
                fuelType
                mileage
                color
                isAvailable
            }
        }
        """
        result = self.execute_query(query, {'id': str(car_id)})
        return result.get('car') if result else None
    
    def get_available_cars(self):
        """Get available cars"""
        query = """
        query GetAvailableCars {
            availableCars {
                id
                brand
                model
                year
                price
                description
                imageUrl
                category
                transmission
                fuelType
                mileage
                color
                isAvailable
            }
        }
        """
        result = self.execute_query(query)
        return result.get('availableCars', []) if result else []
    
    def search_cars(self, search_query):
        """Search cars"""
        query = """
        query SearchCars($query: String!) {
            searchCars(query: $query) {
                id
                brand
                model
                year
                price
                description
                imageUrl
                category
                transmission
                fuelType
                mileage
                color
                isAvailable
            }
        }
        """
        result = self.execute_query(query, {'query': search_query})
        return result.get('searchCars', []) if result else []

class OrderService(GraphQLService):
    def __init__(self):
        super().__init__(Config.ORDER_SERVICE_URL)
    
    def create_order(self, order_data):
        """Create new order"""
        query = """
        mutation CreateOrder($input: OrderInput!) {
            createOrder(input: $input) {
                id
                userId
                totalAmount
                status
                createdAt
                items {
                    id
                    carId
                    quantity
                    price
                }
            }
        }
        """
        result = self.execute_query(query, {'input': order_data})
        return result.get('createOrder') if result else None
    
    def get_user_orders(self, user_id):
        """Get orders for a user"""
        query = """
        query GetUserOrders($userId: ID!) {
            ordersByUser(userId: $userId) {
                id
                userId
                totalAmount
                status
                createdAt
                items {
                    id
                    carId
                    quantity
                    price
                }
            }
        }
        """
        result = self.execute_query(query, {'userId': user_id})
        return result.get('ordersByUser', []) if result else []
    
    def get_order(self, order_id):
        """Get order by ID"""
        query = """
        query GetOrder($id: ID!) {
            order(id: $id) {
                id
                userId
                totalAmount
                status
                createdAt
                items {
                    id
                    carId
                    quantity
                    price
                }
            }
        }
        """
        result = self.execute_query(query, {'id': order_id})
        return result.get('order') if result else None

class CarPayService(GraphQLService):
    def __init__(self):
        super().__init__(Config.CARPAY_URL)
    
    def create_payment(self, payment_data):
        """Create payment via CarPay"""
        query = """
        mutation CreatePayment($input: PaymentInput!) {
            createPayment(input: $input) {
                id
                orderId
                amount
                status
                createdAt
            }
        }
        """
        result = self.execute_query(query, {'input': payment_data})
        return result.get('createPayment') if result else None