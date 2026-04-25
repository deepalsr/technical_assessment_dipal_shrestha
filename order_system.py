# constant data for products and order
products = [
    {"product_id": "P1", "name": "Shampoo", "stock": 10},
    {"product_id": "P2", "name": "Soap", "stock": 20},
    {"product_id":"P3", "name": "Toothpaste", "stock": 15}
]
order = {
    "order_id": "O1001",
    "items": [
        {"product_id": "P1", "quantity": 2},
        {"product_id": "P2", "quantity": 5}
    ]
}

def process_order(order, products):
    # Create a product inventory dictionary for quick lookup
    inventory = {p["product_id"]: p for p in products}
    items = order.get ("items", [])

    #Edge case: No items in the order
    if not items:
        return {"status": "error","message": "No items in the order."}

    #edge case: Duplicate product_id in the order
    seen = set()
    for item in items:
        pid = item['product_id']
        if  pid in seen:
            return {"status": "error", "message": f"Duplicate product_id {pid} in order."}
        seen.add(pid)

    # Check stock availability for each item
    for item in items:
        pid = item["product_id"]
        qty = item ["quantity"]
        if pid not in inventory:
            return {"status": "error", "message": f"Product {pid} not found."}

        if inventory[pid]["stock"] < qty:
            name= inventory[pid]["name"]
            available = inventory[pid]["stock"]
            return {"status": "error",
            "message": f"Insufficient stock for {name}. Available: {available}, Requested: {qty}"
            }

    # If all checks pass, process the order
    for item in items:
        inventory[item["product_id"]]["stock"] -= item["quantity"]

    updated_stock = [
        {"product_id": p["product_id"], "name": p["name"], "stock": p["product_id"]["stock"]}
        for p in products
]

