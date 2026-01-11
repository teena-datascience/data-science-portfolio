# OLAP Cube: Supplier & Product Analysis

## Goal
Demonstrate advanced SQL analytics using **GROUP BY, CUBE, and ROLLUP** on supplier, product, and transaction data.  
The project creates a cube to analyze total transaction quantities, values, and prices at multiple aggregation levels.

---

## Tools Used
- SQL (T-SQL / SQL Server or any RDBMS supporting CUBE/ROLLUP)
- Concepts: GROUP BY, CUBE, ROLLUP, Aggregations, Subqueries, Multidimensional Analysis

---

## Approach
1. **Cube Creation**
   - Joined `Tb_Supplier`, `Tb_Product`, and `Tb_Offers` tables
   - Aggregated data with SUM, MAX, MIN for quantity and transaction value
   - Used `GROUP BY CUBE` and `ROLLUP` to generate multiple aggregation levels

2. **Analytical Queries Using Cube**
   - **Query 1:** Total transaction value by supplier and product packaging  
   - **Query 2:** Volume of milk offered by each supplier in Wisconsin  
   - **Query 3:** Maximum price for each product offered in Madison  
   - **Query 4:** Product offered in largest quantity per supplier city  
   - **Query 5:** City where each product is offered at the lowest price  

---

## Key Skills Demonstrated
- OLAP and multidimensional analysis  
- Creating and querying cubes for business insights  
- Complex filtering using NULLs to select aggregation levels  
- Subqueries for per-group calculations  
- Data-driven decision support using SQL  

---

## File
- `olap_cube_supplier_product.sql` → Contains cube creation and analytical queries
