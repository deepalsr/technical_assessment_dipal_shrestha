# Data for products and an example order
products = [
    {"product_id": "P1", "name": "Shampoo",    "stock": 10},
    {"product_id": "P2", "name": "Soap",       "stock": 20},
    {"product_id": "P3", "name": "Toothpaste", "stock": 15}
]

order = {
    "order_id": "O1001",
    "items": [
        {"product_id": "P1", "quantity": 2},
        {"product_id": "P2", "quantity": 5}
    ]
}

# Process the order and update stock levels
def process_order(products, order):
    # Create a product lookup for easy access
    inventory = {p["product_id"]: p for p in products}
    items = order.get("items", [])
    # edge case: empty order
    if not items:
        return {"status": "error", "message": "Order has no items."}
    
    # edge case: duplicate product in order
    seen = set()
    for item in items:
        pid = item["product_id"]
        if pid in seen:
            return {"status": "error", "message": f"Duplicate product ID '{pid}' in order."}
        seen.add(pid)

    #validate products and stock
    for item in items:
        pid = item["product_id"]
        qty = item["quantity"]
        
        # edge case: product does not exist
        if pid not in inventory:
            return {"status": "error", "message": f"Product '{pid}' does not exist."}
        
        # edge case: insufficient stock
        if inventory[pid]["stock"] < qty:
            name = inventory[pid]["name"]
            available = inventory[pid]["stock"]
            return {
                "status": "error",
                "message": f"Not enough stock for {name}. Available: {available}, Requested: {qty}"
            }

    for item in items:
        inventory[item["product_id"]]["stock"] -= item["quantity"]

    updated_stock = [
        {"product_id": p["product_id"], "name": p["name"], "stock": p["stock"]}
        for p in products
    ]

    return {
        "status": "success",
        "message": f"Order {order['order_id']} processed successfully.",
        "updated_stock": updated_stock
    }


print("-- Normal order --")
print(process_order(products, order))

print("\n-- Empty order --")
print(process_order(products, {"order_id": "O1002", "items": []}))

print("\n-- Product does not exist --")
print(process_order(products, {"order_id": "O1003", "items": [{"product_id": "P99", "quantity": 1}]}))

print("\n-- Insufficient stock --")
print(process_order(products, {"order_id": "O1004", "items": [{"product_id": "P1", "quantity": 999}]}))

print("\n-- Duplicate product in order --")
print(process_order(products, {"order_id": "O1005", "items": [
    {"product_id": "P1", "quantity": 1},
    {"product_id": "P1", "quantity": 2}
]}))