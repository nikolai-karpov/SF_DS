import pandas as pd

# Для непосредственного считывания содержимого файла используем функцию read_json() 
df = pd.read_json('homework/data/recipes.json') # Создаём объект DataFrame, загружая содержимое файла recipes.json

all_ingredients = set() # Создаем пустое множество для хранения реестра уникальных ингредиентов

# Организуем цикл, в котором будем перебирать наименования всех ингредиентов DataFrame 

for ingredients in df['ingredients']:   # Начинаем перебор всех ингредиентов, входящих в состав текущего блюда
    for ingredient in ingredients:
        all_ingredients.add(ingredient)
    

# Какое количество уникальных ингредиентов в нашем DataFrame?
print('Кол-во уникальных ингредиентов: ', len(all_ingredients))


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
for ingredient_name in all_ingredients: # Последовательно перебираем ингредиенты в реестре all_ingredients
    df[ingredient_name] = df['ingredients'].apply(contains) # В DataFrame cоздаем столбец с именем текущего ингредиента применив к столбцу ingredients функцию, созданную нами на предыдущем этапе
                                                            # и заполняем его единицами и нулями, используя ранее созданную функцию contains
                                                            
df['ingredients'] = df['ingredients'].apply(len)            # Заменяем список ингредиентов в рецепте на их количество 