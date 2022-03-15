import pandas as pd

bronze_path = './Root/data/bronze_top.csv'
silver_path = './Root/data/silver_top.csv'
"""
Объедините две таблицы по странам таким образом, чтобы в результат вошли данные только о тех странах, 
которые есть в обоих рейтингах. 
При этом в качестве суффиксов для столбца c числом медалей укажите строки "_bronze" и "_silver", 
чтобы столбцы можно было различать.
Результат занесите в переменную merged.
"""
bronze = pd.read_csv(bronze_path)
silver = pd.read_csv(silver_path)

merged= bronze.merge(
    silver, 
    on='Country', 
    how='inner', 
    right_index=True, 
    left_index=True, 
    suffixes=('_bronze', '_silver')
    )


print(bronze)
print(silver)
print(merged)