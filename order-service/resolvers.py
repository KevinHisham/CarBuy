from ariadne import QueryType, MutationType
from database import (
    get_all_orders, get_order_by_id, get_orders_by_user, get_orders_by_car,
    get_orders_by_status, get_order_stats, create_order, update_order,
    cancel_order, confirm_payment
)

query = QueryType()
mutation = MutationType()

def order_to_dict(order_row):
    """Convert database row to dictionary"""
    if not order_row:
        return None
    
    return {
        "id": str(order_row["id"]),
        "userId": str(order_row["user_id"]),
        "carId": str(order_row["car_id"]),
        "totalAmount": float(order_row["total_amount"]),
        "status": order_row["status"],
        "paymentStatus": order_row["payment_status"],
        "paymentMethod": order_row["payment_method"],
        "notes": order_row["notes"],
        "createdAt": order_row["created_at"],
        "updatedAt": order_row["updated_at"]
    }

@query.field("orders")
def resolve_orders(*_):
    orders = get_all_orders()
    return [order_to_dict(order) for order in orders]

@query.field("order")
def resolve_order(_, info, id):
    order = get_order_by_id(int(id))
    return order_to_dict(order)

@query.field("ordersByUser")
def resolve_orders_by_user(_, info, userId):
    orders = get_orders_by_user(int(userId))
    return [order_to_dict(order) for order in orders]

@query.field("ordersByCar")
def resolve_orders_by_car(_, info, carId):
    orders = get_orders_by_car(int(carId))
    return [order_to_dict(order) for order in orders]

@query.field("ordersByStatus")
def resolve_orders_by_status(_, info, status):
    orders = get_orders_by_status(status)
    return [order_to_dict(order) for order in orders]

@query.field("orderStats")
def resolve_order_stats(*_):
    stats = get_order_stats()
    return {
        "totalOrders": stats['total_orders'],
        "pendingOrders": stats['pending_orders'],
        "completedOrders": stats['completed_orders'],
        "totalRevenue": stats['total_revenue']
    }

@mutation.field("createOrder")
def resolve_create_order(_, info, input):
    try:
        order = create_order(
            user_id=int(input["userId"]),
            car_id=int(input["carId"]),
            total_amount=input["totalAmount"],
            payment_method=input.get("paymentMethod"),
            notes=input.get("notes")
        )
        return order_to_dict(order)
    except Exception as e:
        raise Exception(f"Failed to create order: {str(e)}")

@mutation.field("updateOrder")
def resolve_update_order(_, info, id, input):
    try:
        order = update_order(int(id), **input)
        if not order:
            raise Exception("Order not found")
        return order_to_dict(order)
    except Exception as e:
        raise Exception(f"Failed to update order: {str(e)}")

@mutation.field("cancelOrder")
def resolve_cancel_order(_, info, id):
    try:
        order = cancel_order(int(id))
        if not order:
            raise Exception("Order not found")
        return order_to_dict(order)
    except Exception as e:
        raise Exception(f"Failed to cancel order: {str(e)}")

@mutation.field("confirmPayment")
def resolve_confirm_payment(_, info, id):
    try:
        order = confirm_payment(int(id))
        if not order:
            raise Exception("Order not found")
        return order_to_dict(order)
    except Exception as e:
        raise Exception(f"Failed to confirm payment: {str(e)}")