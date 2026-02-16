```sql
select city, count(city) from supermarket_sales ss group by ss.city;

select gender, count(gender) from supermarket_sales ss group by ss.gender;

select ss."Product line", count(ss."Product line") from supermarket_sales ss group by ss."Product line";

select city, "Product line", count("Product line") as orders_cnt
from supermarket_sales
group by city, "Product line"
order by 3 desc;

select city, "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by city,  "Product line"
order by 4 desc;

select city, "Product line", count("Product line") as orders_cnt, avg("total") as avg_check
from supermarket_sales
group by city,  "Product line"
order by 4 desc;

select gender, "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by gender,  "Product line"
order by 4 desc;

select "Customer type", "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by "Customer type", "Product line"
order by 4 desc;

select "Product line", count("Product line") as order_cnt, "Date"
from supermarket_sales
group by "Product line", "Date"
order by 2 desc;
```