import pandas as pd

df = pd.read_csv('homework/data/recipes.csv') # Создаём DataFrame, читаем данные из файла в переменную df

# Создание списка, содержащего перечень id всех блюд
list_id = list(df['id'])

# Создание списка ингредиентов
all_ingredients = set() # Создаем пустое множество для хранения реестра уникальных ингредиентов

# Организуем цикл, в котором будем перебирать наименования всех ингредиентов DataFrame 
for ingredients in df['ingredients']:   # Начинаем перебор всех ингредиентов, входящих в состав текущего блюда
    for ingredient in ingredients:
        all_ingredients.add(ingredient)

print(list_id)