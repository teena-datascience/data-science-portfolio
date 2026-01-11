--1) List full transaction data relating to suppliers from Madison and
--consumers from Stevens Point where transaction value is higher than
--$10,000 (show supplier, consumer and product names, quantity and price)?

SELECT S.Name as Supplier_name ,
C.Name as Consumer_name, 
P.Name as Product_name, 
T.Quantity, 
T.Price
FROM
Tb_Supplier S
JOIN Tb_Transactions T ON S.Supp_ID = T.Supp_ID
JOIN Tb_Product P ON P.Prod_ID= T.Prod_ID
JOIN Tb_Consumer C ON C.Con_ID = T.Con_ID
WHERE S.City= 'Madison'
AND C.City='Stevens Point'
AND (T.Price * T.Quantity)> 10000;

--2. Name of suppliers offering both computers and oranges? (do not use set
--operations)
SELECT Name 
FROM Tb_Supplier 
Where Supp_ID IN
(SELECT DISTINCT Supp_ID
FROM Tb_Offers O JOIN Tb_Product P
ON o.Prod_ID=p.Prod_ID
WHERE P.Name= 'Computer'
)
AND Supp_ID IN
(SELECT DISTINCT Supp_ID
FROM Tb_Offers O JOIN Tb_Product P
ON o.Prod_ID=p.Prod_ID
WHERE P.Name= 'Orange'
);

--3. Name of suppliers from Wausau or offering computers or offering
--oranges?
SELECT DISTINCT s.Name 
FROM Tb_Supplier s
JOIN Tb_Offers o  ON  s.Supp_ID= o.Supp_ID
JOIN Tb_Product p ON p.Prod_ID=o.Prod_ID
Where p.Name='Computer' OR p.Name='Orange' OR s.City='Wausau'
;



--4. Name of suppliers offering computer, auto and orange?
SELECT Name
FROM Tb_Supplier
Where Supp_ID IN
(SELECT DISTINCT Supp_ID
FROM Tb_Offers o JOIN Tb_Product p
ON o.Prod_ID= p.Prod_ID
WHERE p.Name='Computer')
AND Supp_ID IN
(SELECT DISTINCT Supp_ID
FROM Tb_Offers o JOIN Tb_Product p
ON o.Prod_ID= p.Prod_ID
WHERE p.Name='Auto'
)
AND Supp_ID IN
(SELECT DISTINCT Supp_ID
FROM Tb_Offers o JOIN Tb_Product p
ON o.Prod_ID= p.Prod_ID
WHERE p.Name='Orange');

--5. Name of products not offered in Chicago?
SELECT DISTINCT p.Name 
FROM Tb_Product p
WHERE p.Prod_ID NOT IN (
    SELECT o.Prod_ID 
    FROM Tb_Offers o
    JOIN Tb_Supplier s ON o.Supp_ID = s.Supp_ID
    WHERE s.City = 'Chicago');

--6. Name of consumers requesting only computers?
SELECT DISTINCT c.Name
FROM Tb_Consumer c
WHERE c.Con_ID in
(
SELECT r.Con_ID
FROM  Tb_Requests r 
JOIN Tb_Product p ON p.Prod_ID= r.Prod_ID
WHERE p.Name= 'Computer'
)
AND c.Con_ID NOT IN
(
SELECT DISTINCT r.Con_ID
FROM Tb_Requests r 
JOIN Tb_Product p ON p.Prod_ID= r.Prod_ID
WHERE p.Name!= 'Computer'
)
;

--7. Name of supplier cities where none of the suppliers has any offer?
SELECT s.City
FROM Tb_Supplier s 
WHERE City NOT IN 
(SELECT DISTINCT City
FROM Tb_Offers o, Tb_Supplier ts
WHERE ts.Supp_ID=o.Supp_ID
);


--8. Name of products requested by all consumers?
SELECT p.Name
FROM Tb_Product p
WHERE NOT EXISTS (SELECT *
		FROM Tb_Consumer c
		WHERE NOT EXISTS (SELECT *
			FROM Tb_Requests r
			WHERE p.Prod_ID= r.Prod_ID
			AND r.Con_ID= c.Con_ID));


--9. Product name and supplier having the largest offer (as quantity) for that
--product?
SELECT DISTINCT p.Name AS 'Product Name', 
s.Name AS 'Supplier Name', 
o.Quantity
FROM Tb_Product p 
JOIN Tb_Offers o ON p.Prod_ID= o.Prod_ID
JOIN Tb_Supplier s ON s.Supp_ID= o.Supp_ID
WHERE o.Quantity = (SELECT MAX(Quantity)
					FROM Tb_Offers
					WHERE Prod_ID= p.Prod_ID);


--10. Product name and city where that product sold best, as in largest total
--quantity?

SELECT 
P.Name, 
C.City, 
SUM(T.Quantity) AS Total_Quantity
FROM 
Tb_Product P
JOIN Tb_Transactions T ON P.Prod_ID = T.Prod_ID
JOIN Tb_Consumer C ON T.Con_ID = C.Con_ID
GROUP BY 
P.Name, C.City
HAVING 
SUM(T.Quantity) = (
SELECT 
MAX(tot_qty)
FROM (
SELECT 
SUM(T1.Quantity) AS tot_qty
FROM 
Tb_Product P1
JOIN Tb_Transactions T1 ON P1.Prod_ID = T1.Prod_ID
JOIN Tb_Consumer C1 ON T1.Con_ID = C1.Con_ID
WHERE 
P1.Name = P.Name
GROUP BY 
C1.City
) as dat
);


--(Extra Credit 2%) Name of products requested in all consumer cities other
--than Stevens Point?

SELECT Name
FROM Tb_Product P
WHERE NOT EXISTS (SELECT *
				  FROM Tb_Consumer C
				  WHERE C.City <> 'Stevens Point'
				  AND NOT EXISTS (SELECT *
				  FROM Tb_Consumer , Tb_Requests r
				  WHERE  P.Prod_ID=r.Prod_ID
				  AND r.Con_ID= Tb_Consumer.Con_ID
				  AND C.City=City
				));

