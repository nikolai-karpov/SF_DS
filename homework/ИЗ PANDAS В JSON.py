import pandas as pd
from pprint import pprint

df = pd.read_csv('homework/data/recipes.csv') # Создаём DataFrame, читаем данные из файла в переменную df

all_ingredients = set() # Создаем пустое множество для хранения реестра уникальных ингредиентов

# Организуем цикл, в котором будем перебирать наименования всех ингредиентов DataFrame 
for ingredients in df['ingredients']: # Начинаем перебор всех блюд входящих в список
    for ingredient in ingredients:    # Начинаем перебор всех ингредиентов, входящих в состав текущего блюда
        all_ingredients.add(ingredient )        # Добавляем уникальный ингредиент в реестр
    
print('all_ingredients: ', all_ingredients)
# Создание и заполнение столбцов
def contains(ingredient_list):
    """Функцию для заполнения значения в каждой ячейке.
        Функция будет проверять наличие конкретного ингредиента в столбце ingredients для текущего блюда 

    Args:
        args (list): [Значение в ячейке столбца ingredients текущего рецепта]

    Returns:
        [int]: [Возвращать 1, если ингредиент есть в рецепте, 0, если он отсутствует]
    """
    if ingredient_name in ingredient_list:  # Если ингредиент есть в текущем блюде,
        return 1                            # возвращаем значение 1
    else:                                   # Если ингредиента нет в текущем блюде,
        return 0                            # возвращаем значение 0
    
    
# Для каждого ингредиента создадим в DataFrame столбец с соответствующим названием 
for ingredient_name in all_ingredients:                     # Последовательно перебираем ингредиенты в реестре all_ingredients
    df[ingredient_name] = df['ingredients'].apply(contains) # В DataFrame cоздаем столбец с именем текущего ингредиента применив к столбцу ingredients функцию, созданную нами на предыдущем этапе
                                                            # и заполняем его единицами и нулями, используя ранее созданную функцию contains
                                                            
df['ingredients'] = df['ingredients'].apply(len)            # Заменяем список ингредиентов в рецепте на их количество 


list_id = list(df.id) # Создаем список уникальных значений id-блюд
 
# Создание списка ингредиентов
ingredients = list(df.columns)[3:] # Создаем список уникальных значений ингредиентов
print(ingredients)

def make_list(row):
    """Функция трансформирует строку DataFrame df в список

    Args:
        arg (str): На вход получает строку, содержащую данные об одном рецепте

    Returns:
        [list]: Возвращает перечень ингредиентов, входящих в состав этого блюда в виде списка
    """
    ingredient_list=[] # Создаём пустой список ингредиентов текущего блюда

    for ingredient in ingredients: # Последовательно перебираем ингрединеты из реестра
        if row[ingredient].item()==1: # Если текущий ингредиент входит в состав текущего блюда
            ingredient_list.append(ingredient) # Добавляем ингредиент в список ингредиентов текущего блюда
            
    return ingredient_list # Возвращаем сформированный спиок ингредиентов


new_recipes = []                # Создаём пустой список для хранения итоговой структуры

for current_id in list_id:      # Организуем цикл с параметром current_id
    cuisine = df[df['id'] == current_id]['cuisine'].iloc[0]     # Получаем значение соответствующей кухни, 
                                                                # применив фильтр по текущему значению параметра цикла к DataFrame;
    current_ingredients = make_list(df[df['id'] == current_id]) # Получаем перечень ингредиентов, входящих в состав текущего блюда
    #print(current_ingredients)
    current_recipe = {
        'cuisine': cuisine, 
        'id': int(current_id), 
        'ingredients': current_ingredients
        }                                           # Создаём текущий словарь
    new_recipes.append(current_recipe)              # Добавляем созданный словарь к списку
    

#pprint(new_recipes)