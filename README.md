# technical_assessment_dipal_shrestha
This is my repository for the technical assessment
## How to Run

'''bash
python order_system.py
'''

No external dependencies. Just plain Python
Once running:
-Type **yes** to place a new order
-Type anything else to exit the program

---
## Section 1 - Coding Task: Order & Inventory System

### Approach
I kept it simple. The core idea is:
1. Build a dict form the product list so lookups are O(1)
2. Validate the product ID at a input time - user can.t proceed with a fake ID
3. Check all remaining edge cases *before* touching any stock- so we never do a partial deduction
4. If everything passes, deduct and return the updated stock

Order IDs auto-increment starting from 01001. Each new order gets the next ID automatically.

### Edge Cases handled
- **Empty order**
- **Invalid Product ID**
- **Insufficient stock**
- **Duplicate product in the order**

### Bonus - Scalability (10,000 orders/minute)
The current setup is a single-process, in-memory thing. At 10k orders/minute the breaks in a few obvious ways.

Changes I would make:
- Make inventory to a proper database, Postgres is my suggestion removing race condtion and allowing multi user. use atomic opertaions for stock deduction
- Run multiple worker processes behind a load balancer
- Put incoming orders in queue so spikes dont crash the system
- Add a caching layer for product lookups 


## Section 2 - Warehouse Allocation

### Current State

| Product | Warehouse A | Warehouse B|
|---------|-------------|------------|
| Shampoo | 5 | 10|
|Soap| 10| 5|

### Order Requirements 
- P1: 8 units
- P2: 6 units



