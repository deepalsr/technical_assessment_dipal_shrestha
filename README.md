# technical_assessment_dipal_shrestha
This is my repository for the technical assessment
## How to Run

```bash
python order_system.py
```

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

### Q1 - Allocation Plan

**P1 (need 8):**
- Take all 8 from Warehouse B 
- No need to touch warehouse A

**P2 (need 6):**
- Take all 6 from Warehouse A
- No need to touch Warehouse B


### Q2 - Strategy
I went with **minimize shipment splits where possible**.
For P2, Warehouse A had enough its own so I kept it to a single source, simpler logistics. For P1 same reasoning.
But for delivery speed, it depends on which one is closer or nearest to the user, but not having the data is main reason I went with no pertial deduction keeping the stock as it is in warehouses where the quantity is insufficient.

### Q3 - assumptions
- Both warehouses have the same shipping cost and delivery time.
- The order must be fully fullfilled
- Stock numbers are accurate
- No constraints regarding the warehouse trasnfer requirements.

---


### Section 3 - Quantitative & Logical Reasoning

### Q1 - Caluclation
In every 2 seconds, 5 parallel orders are processed.
In 1 minute, there are 60 seconds.
In 1 minute, 60/2 * 5 = 150 orders/minute

**The system can handle 150 orders/ minutes**

### Q2 - Overload

The system normal capacity is 150 orders/min. When the traffic spikes at 300 orders/min
The follwing effects occur:
- The queue grows continuously, 150 orders pile up every minute
- Response time increases as orders wait longer
- If there is no queue limit, memory fills up and system crashes
- If there is a limit, new orders start getting rejected.

The failure of mode is either an oit of memory crash or a flood  of rejected/timed-out request- depending on how queue is set.

### Q3 -Improvement

**Add more parallel workers.**
 If we go from 5 to 10 workers at the same rate, throughput doubles to exactly where we want. So my suggestion is horizontal scaling. This helps because we are dealign with a throughput issue here, and we dont need to change our system. This is like adding more procesors/threads.



