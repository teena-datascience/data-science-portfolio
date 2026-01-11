# Supplier & Consumer SQL Queries

## Goal
Demonstrate proficiency in SQL by solving real-world transaction and supply chain problems using multiple tables, joins, subqueries, aggregations, and set operations.

---

## Tools Used
- SQL (MySQL / PostgreSQL / any relational DBMS)
- Concepts: Joins, Subqueries, NOT IN, NOT EXISTS, Aggregation, Grouping

---

## Queries Overview

1. **Transactions over $10,000**  
   List supplier, consumer, product, quantity, and price for transactions meeting certain city and value conditions.

2. **Suppliers offering both computers and oranges**  
   Find suppliers who offer multiple specified products.

3. **Suppliers from Wausau or offering computers/oranges**  
   Combine city and product-based filtering using OR.

4. **Suppliers offering computer, auto, and orange**  
   Multi-condition filtering using subqueries and AND logic.

5. **Products not offered in Chicago**  
   Identify products absent in a specific city using `NOT IN`.

6. **Consumers requesting only computers**  
   Use `NOT IN` and subqueries to filter for exclusive requests.

7. **Supplier cities with no offers**  
   Identify cities where suppliers do not have any active offers.

8. **Products requested by all consumers**  
   Use `NOT EXISTS` to solve "for all" type queries.

9. **Largest offer per product**  
   Find the supplier offering the highest quantity for each product.

10. **City where a product sold the most**  
    Identify city with largest total quantity sold per product.


---

## Key Skills Demonstrated
- Complex multi-table joins  
- Subqueries and nested queries  
- Aggregations with `SUM`, `MAX`  
- Advanced filtering (`NOT IN`, `NOT EXISTS`)  
- Data analysis and decision-making using SQL  

---

## File
- `supplier_consumer_queries.sql` → Contains all 10+ SQL queries
