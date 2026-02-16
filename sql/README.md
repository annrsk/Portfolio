*Несколько запросов для просмотра базовых показателей магазина.*

Количество заказов в магазине в городах:
```sql
select city, count(city) as cnt_orders from supermarket_sales ss group by ss.city;
```
Количество заказов в магазине у мужчин и женщин:
```sql
select gender, count(gender) as cnt_orders from supermarket_sales ss group by ss.gender;
```
Количество заказов в магазине по категориям:
```sql
select ss."Product line", count(ss."Product line") as cnt_orders from supermarket_sales ss group by ss."Product line";
```

Посмотрим количество заказов каждой категории в каждом городе:
```sql
select city, "Product line", count("Product line") as orders_cnt
from supermarket_sales
group by city, "Product line"
order by 3 desc;
```

Посмотрим на выручку магазина по категориям в каждом городе: (до вычета налогов)
```sql
select city, "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by city,  "Product line"
order by 4 desc;
```
Средний чек заказа каждой категории по городам:
```sql
select city, "Product line", count("Product line") as orders_cnt, avg("total") as avg_check
from supermarket_sales
group by city,  "Product line"
order by 4 desc;
```

Выручка магазина по типам покупателей: (до вычета налогов) 
```sql
select "Customer type", "Product line", count("Product line") as orders_cnt, sum("Gross income") as total_gross
from supermarket_sales
group by "Customer type", "Product line"
order by 4 desc;
```

Количество заказов каждой категории по дням:
```sql
select "Product line", count("Product line") as order_cnt, "Date"
from supermarket_sales
group by "Product line", "Date"
order by 2 desc;
```