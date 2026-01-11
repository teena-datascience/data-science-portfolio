# Transactions Cube SQL Queries

## Goal
Demonstrate multidimensional OLAP analysis using a **Transactions Cube** (`Tb_Transactions_Cube`) to extract insights on supplier-consumer-product transactions.

The project shows how to aggregate transactional data at multiple levels, including supplier, consumer, product, city, and state, and compare quantities and sales across different dimensions.

---

## Tools Used
- SQL (T-SQL / SQL Server)
- Concepts: GROUP BY, CUBE, ROLLUP, Aggregations, NULL handling, Full Outer Join

---

## Queries Overview

1. **Aggregates by supplier and product**  
   Summarize total transactions by combinations of supplier and product names.

2. **Aggregates by supplier states**  
   Total transaction aggregates at the state level.

3. **Transactions by supplier-city and consumer-city**  
   Count of transactions for each supplier-city / consumer-city pair.

4. **Product quantities sold by Wisconsin suppliers**  
   Total quantity of each product sold by Wisconsin suppliers.

5. **Quantity of sales aggregated by product and supplier state**  
   Summarizes total quantities per product and supplier state.

6. **Quantity of computer sales by Wisconsin suppliers**  
   Aggregates for a specific product (Computer).

7. **Auto sales from Wisconsin suppliers to Illinois consumers**  
   Shows supplier-consumer-level aggregation for a specific product.

8. **Products sold by Madison suppliers to Illinois consumers**  
   Multi-level aggregation by product, supplier, and consumer.

9. **Product sales by supplier Bernstein to Chicago consumers**  
   Specific supplier and consumer analysis.

10. **Milk sales by Bernstein to Chicago consumers**  
    Product-specific transactional detail.

11. **Extra Credit:** Compare quantities Madison→Chicago vs Chicago→Madison  
    Demonstrates use of **FULL OUTER JOIN** for comparative OLAP analysis.

---

## Key Skills Demonstrated
- Advanced OLAP queries on transactional data  
- Aggregations at multiple hierarchical levels  
- NULL handling for level-specific aggregation in cubes  
- Using subqueries and full outer joins for comparative analysis  
- Extracting actionable business insights from transactional datasets  

---

## File
- `transactions_cube_queries.sql` → Contains all 11 queries on `Tb_Transactions_Cube`
