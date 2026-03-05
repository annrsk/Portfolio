import pandas as pd
import matplotlib.pyplot as plt
import math

df = pd.read_excel('выборка2.xlsx', engine='openpyxl')
df['Выручка'] = df['Количество'] * df['Цена']
print(df)

#линейный график
plt.figure(figsize=(24, 12))
x = df['Дата']
y = df['Выручка']
plt.title('Линейный график зависимости выручки от даты')
plt.plot(x, y, marker='*')
plt.xlabel('date')
plt.ylabel('income')
plt.show()

#диаграмма рассеивания
plt.figure(figsize=(24,12))
x = df['Количество']
y = df['Выручка']
plt.scatter(x, y, color='pink')
plt.title('График рассеивания')
plt.xlabel('Количество')
plt.ylabel('Выручка')
plt.show()


#гистограмма
x = 1+(3.322*math.log(38))
plt.hist(df['Выручка'], bins=int(x), color='pink', edgecolor='white')
plt.title('Гистограмма')
plt.xlabel('Выручка')
plt.ylabel('Частота')
plt.show()

#гистограмма накопленной частоты
x = 1+(3.322*math.log(38))
plt.hist(df['Количество'], bins=int(x), cumulative=True, color='pink', edgecolor='white')
plt.title('Гистограмма накопленной частоты')
plt.xlabel('Количество')
plt.ylabel('Частота')
plt.show()