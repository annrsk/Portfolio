import pandas as pd

df = pd.read_excel('ПР_№1_учебная выборка (ПЗ-2).xlsx', engine='openpyxl')
df['Дата'] = pd.to_datetime(df['Дата'])

print(f'Первые 5 строк таблицы:\n{df.head(5)}')

count_orig = df.count()
print(f'Количество данных до подготовки:\n{count_orig}')

numb_col = df.select_dtypes('number')
max_value = numb_col.max()
min_value = numb_col.min()
mean_value = numb_col.mean()
print(f'Макисимальное значение:\n{max_value}\nМинимальное значение:\n{min_value}\nСреднее значение:\n{mean_value}')

import numpy as np
mean_salary = df[df['Продажи_RUB'] > 0]['Продажи_RUB'].mean()
df['Продажи_RUB'] = np.where(df['Продажи_RUB'] < 0, mean_salary, df['Продажи_RUB'])
print(df)

df_del = df.copy()
df_del = df_del.dropna()
print(f'Выборка после удаления пустых строк:\n{df_del}')

df_mean = df.copy()
values = df.select_dtypes(include='number')
mean_val = values.mean()
df_mean.fillna(mean_val, inplace=True)
print(f'Выборка после замены пустых строк:\n{df_mean}')

df_delId = df_del.drop(columns='ID')
print(f'Выборка после удаления столбца ID:\n{df_delId}')

count = df_delId.count()
print(f'Количество данных до удаления выбросов:\n{count}')

number_colums = df_delId.select_dtypes('number').columns
df_cleaned = df_delId.copy()
for column in number_colums:
    Q1 = df_delId[column].quantile(0.25)
    Q3 = df_delId[column].quantile(0.75)
    IQR = Q3 - Q1
    min_bound = Q1 - 1.5 * IQR
    max_bound = Q3 + 1.5 * IQR
    df_cleaned = df_cleaned[(df_cleaned[column] >= min_bound) & (df_cleaned[column] <= max_bound)]

print(f'Выборка после удаления выбросов:\n{df_cleaned}')

count_new = df_cleaned.count()
print(f'Количество данных после подготовки:\n{count_new}')

pd.set_option('display.float_format', '{:.2f}'.format)
print(f'Финальная выборка:\n{df_cleaned}')
