```sql
select city, count(city) from supermarket_sales ss group by ss.city;
```

```sql
select gender, count(gender) from supermarket_sales ss group by ss.gender;
```

```sql
select ss."Product line", count(ss."Product line") from supermarket_sales ss group by ss."Product line";
```

```sql
select city, "Product line", count("Product line") as orders_cnt
from supermarket_sales
group by city, "Product line"
order by 3 desc;
```

```sql
select city, "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by city,  "Product line"
order by 4 desc;
```

```sql
select city, "Product line", count("Product line") as orders_cnt, avg("total") as avg_check
from supermarket_sales
group by city,  "Product line"
order by 4 desc;
```

```sql
select gender, "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by gender,  "Product line"
order by 4 desc;
```

```sql
select "Customer type", "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by "Customer type", "Product line"
order by 4 desc;
```

```sql
select "Product line", count("Product line") as order_cnt, "Date"
from supermarket_sales
group by "Product line", "Date"
order by 2 desc;
```