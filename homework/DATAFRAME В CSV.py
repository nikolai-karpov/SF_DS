import pandas as pd
pd.__version__
df = pd.read_json('homework/data/recipes.json') # Создаём объект DataFrame, загружая содержимое файла recipes.json
df.to_csv('homework/data/recipes.csv', index = False) # index=False позволит нам не сохранять индексы строк в виде отдельного столбца