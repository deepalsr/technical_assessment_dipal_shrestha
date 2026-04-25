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

def process_order(products, order):
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
        {"product_id": p["product_id"], "name": p["name"], "stock": p["stock"]}
        for p in products
        ]

    return {"status": "success", "message": "Order processed successfully.", "updated_stock": updated_stock}
order_counter = 1001
def take_order_from_user():
    global order_counter
    order_id = f"O{order_counter}"
    order_counter += 1
    print(f"Creating order with ID: {order_id}")
    items = []
    while True:
        product_id = input("Enter product ID (or 'done' to finish): ")
        if product_id.lower() == "done":
            break
        quantity = input(f"\nEnter quantity for {product_id}: ").strip()
        if not quantity.isdigit() or int(quantity) <= 0:
            print("Invalid quantity. Please enter a positive integer.")
            continue
        items.append({"product_id": product_id, "quantity": int(quantity)})
    return {"order_id": order_id, "items": items}


if __name__ == "__main__":
    user_order = take_order_from_user()
    result = process_order(products, user_order)
    print("\nOrder Result:")
    print(result)
