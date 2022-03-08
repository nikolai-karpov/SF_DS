import json # Импортируем модуль json
from pprint import pprint # Импортируем функцию pprint()

# ОТКРЫВАЕМ JSON-ФАЙЛ

# десериализация (декодирование данных)
with open('homework/data/recipes.json') as f: # Открываем файл и связываем его с объектом "f"
    recipes = json.load(f) # Загружаем содержимое открытого файла в переменную recipes
    
pprint(recipes) # Выводим на экран содержимое переменной recipes, используя функция pprint()


# ИЗВЛЕКАЕМ ДАННЫЕ ИЗ JSON-ФАЙЛА

