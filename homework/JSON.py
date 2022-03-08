import json # Импортируем модуль json
from pprint import pprint # Импортируем функцию pprint()

# ОТКРЫВАЕМ JSON-ФАЙЛ

# десериализация (декодирование данных)
with open('homework/data/recipes.json') as f:   # Открываем файл и связываем его с объектом "f"
    recipes = json.load(f)                      # Загружаем содержимое открытого файла в переменную recipes
    
#pprint(recipes) # Выводим на экран содержимое переменной recipes, используя функция pprint()


# ИЗВЛЕКАЕМ ДАННЫЕ ИЗ JSON-ФАЙЛА
# Сколько ингредиентов входят в состав первого блюда из предлагаемого списка?
#print(len(recipes[0]['ingredients'])) # Определяем количество ингредиентов в составе первого блюда/рецепта


# К какой кухне относится блюдо с id = 13121?
for dish in recipes:
    if dish['id'] == 13121:
        print(dish['cuisine'])
        
        
# Какое количество уникальных национальных кухонь присутствуют в нашем наборе данных?

# ВАРИАНТ РЕШЕНИЯ С ИСПОЛЬЗОВАНИЕМ СПИСКА
cuisines_list = []  # Создаем пустой список 

for recipe in recipes:                                    # для извлечения всех уникальных значений перебираем элементы списка в цикле.
    if recipe['cuisine'] in cuisines_list:
        pass
    else:
        cuisines_list.append(recipe['cuisine'])             # и последовательно заполнять его уникальными значениями, 
                                                        # доступными по ключу 'cuisine' в каждом из словарей, содержащих информацию о рецептах. 
        
#print(len(cuisines_list))


# ВАРИАНТ РЕШЕНИЯ С ИСПОЛЬЗОВАНИЕМ МНОЖЕСТВА
# использование для хранения данных о разных кухнях множество (set)
cuisines_set = set()  # Создаем множестов 

for recipe in recipes:                                    # для извлечения всех уникальных значений перебираем элементы списка в цикле.
    if recipe['cuisine'] in cuisines_set:
        pass
    else:
        cuisines_set.add(recipe['cuisine'])             # и последовательно заполнять его уникальными значениями, 
                                                        # доступными по ключу 'cuisine' в каждом из словарей, содержащих информацию о рецептах. 
        
#print(len(cuisines_set))


# Какой из национальных кухонь принадлежит самое большое количество рецептов?
from collections import Counter

cuisines_list = []  # Создаем пустой список 

for recipe in recipes:                                    # для извлечения всех уникальных значений перебираем элементы списка в цикле.
    cuisines_list.append(recipe['cuisine'])
    
answer = Counter(cuisines_list)
print(max(answer, key=answer.get)) # Извлекаем значения для всех ключей используя метод get(), 
                                    # выбираем самое максимальное значение (при наличии одинаковых значений будет выбрано первое в словаре) 
                                    # и выводим на экран ключ максимального значения
          

# ИЗ JSON В PANDAS
import pandas as pd             # Импортируем модуль pandas

df = pd.DataFrame(recipes)      # Создаём объект DataFrame из списка recipes 

# Для непосредственного считывания содержимого файла используйте функцию read_json() 
df = pd.read_json('homework/data/recipes.json') # Создаём объект DataFrame, загружая содержимое файла recipes.json
print(df.info())                # Выводим на экран первые строки полученного DataFrame

