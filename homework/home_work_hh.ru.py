from locale import currency
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


hh_data = pd.read_csv('/Volumes/HDD/Dropbox/Data Science/VS CODE/dst-3.0_16_1_hh_database.csv', sep=';')


def get_education(arg):
    arg = ' '.join(arg.split(' ')[:3])
    if 'Высшее' in arg:
        return 'высшее'
    elif 'Неоконченное высшее' in arg:
        return 'неоконченное высшее'
    elif 'Среднее специальное' in arg:
        return 'среднее специальное'
    elif 'Среднее образование' in arg:
        return 'среднее'
    
hh_data['Образование'] = hh_data['Образование и ВУЗ'].apply(get_education)
hh_data = hh_data.drop('Образование и ВУЗ', axis=1)                         # Удаляем ненужны столбец


# Сколько соискателей имеет средний уровень образования (школьное образование)?
#print(hh_data['Образование'].value_counts(dropna=False))


# Создайте признак "Пол" 
# Признак пола должен иметь 2 уникальных строковых значения: 'М' - мужчина, 'Ж' - женщина.
# Создайте признак "Возраст".
# Признак возраста должен быть представлен целыми числами.
def get_gender(args):
    if 'Мужчина ' in args:
        return 'м'
    if 'Женщина ' in args:
        return 'ж'


def get_age(args):
    splitted_args = args.split(',')
    age = splitted_args[1].split(' ')
    return age[2]

hh_data['Пол'] = hh_data['Пол, возраст'].apply(get_gender)

hh_data['Возраст'] = hh_data['Пол, возраст'].apply(get_age)  
hh_data['Возраст'] = hh_data['Возраст'].astype(np.int8)  

percentage_women = hh_data.groupby('Пол')['Пол'].count().transform(lambda x: x / hh_data.shape[0] * 100)
#print('Распределение резюме %', round(percentage_women, 2))
#print('Средний возраст соискателей', round(hh_data['Возраст'].mean(), 1))



 
# Напишите функцию, аргументом которой является строка столбца с опытом работы.
# Функция должна возвращать опыт работы в месяцах
# Не забудьте привести результат к целому числу
def get_experience(arg):
    try:
        args_splited = arg.split(' ')[:6]
        year_key_words = ['лет', 'год', 'года']
        month_key_words = ['месяца', 'месяцев', 'месяц']
        year = 0
        month = 0
        for i in range(len(args_splited)):          # Перебираем переданные слова 
            if args_splited[i] in year_key_words:   # если слово совпадает с ключом
                year =  args_splited[i-1]           # Заносим предыдущее перед ним значение в переменную
            if args_splited[i] in month_key_words:
                month = args_splited[i-1]
        return round((int(year)*12) + (int(month)), 0)        
    except AttributeError:
        hh_data['Опыт работы'].fillna(np.nan)       # Если встречаем данные с которыми нельзя работать заполняем их NaN


hh_data['Опыт работы (месяц)'] = hh_data['Опыт работы'].apply(get_experience)

# Чему равен медианный опыт работы (в месяцах) в нашей таблице?
hh_data['Опыт работы (месяц)'].median()


# Создадим отдельные признаки 
# «Город»
million_cities = ['Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Челябинск', 'Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград' ]

def get_citi(args):
    args_splited = args.split(' ')[:1]
    if 'Москва' in args_splited:
        return 'Москва'
    if 'Санкт-Петербург' in args_splited:
        return 'Санкт-Петербург'
    for i in range(len(args_splited)):
        if args_splited[i] in million_cities:
            return 'город-миллионник'
    else:
        return 'другие'

hh_data['Город'] = hh_data['Город, переезд, командировки'].apply(get_citi)

# Сколько процентов соискателей живут в Санкт-Петербурге?
urban_residents = hh_data.groupby('Город')['Город'].count().transform(lambda x: x / hh_data.shape[0] * 100)
#print('Жители %', round(urban_residents))


def ready_to_move(args):
    result = None
    if ('не готов к переезду' in args) or ('не готова к переезду' in args) or ('не хочу переезжать' in args):
        result = False  
    else:
        result = True
    return result


hh_data['Готовность к переезду'] = hh_data['Город, переезд, командировки'].apply(ready_to_move)
percent_to_move = hh_data.groupby('Готовность к переезду')['Готовность к переезду'].count().transform(lambda x: x / hh_data.shape[0] * 100)
#print(round(percent_to_move), '%')

# «Готовность к командировкам». 
def ready_business_trip(args):
    list_variants = ['готов к командировкам', 'готова к командировкам', 'готов к редким командировкам', 'готова к редким командировкам']
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):         # Перебираем переданные слова 
        if args_splited[i].strip() in list_variants:   # если слово совпадает с ключом
            result = True
        else:
            result = False
    return result


hh_data['Готовность к командировкам'] = hh_data['Город, переезд, командировки'].apply(ready_business_trip)

# Сколько процентов соискателей готовы одновременно и к переездам, и к командировкам?
percent_move_trip = round(hh_data[hh_data['Готовность к переезду'] & hh_data['Готовность к командировкам']].shape[0] / hh_data.shape[0] *100) # Берем кол-во совпадающих значений делим на общее кол-во строк
#print(round(percent_move_trip), '%')


# Преобразование для признаков «Занятость» и «График»

"""Все что я насочинял собирает данные которые ен принимает курс
# Функция для признака "полная занятость"
def get_full_time(args):
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):                      # Перебираем переданные слова 
        if args_splited[i].strip() == 'полная занятость':   # если слово совпадает с ключом
            result = True
        else:
            result = False
        return result

hh_data['полная занятость'] = hh_data['Занятость'].apply(get_full_time)

# Функция для признака "частичная занятость"
def get_part_time(args):
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):                      # Перебираем переданные слова 
        if args_splited[i].strip() == 'частичная занятость':   # если слово совпадает с ключом
            result = True
        else:
            result = False
        return result

hh_data['частичная занятость'] = hh_data['Занятость'].apply(get_full_time)

# Функция для признака "проектная работа"
def get_project_work(args):
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):                   # Перебираем переданные слова 
        if args_splited[i].strip() == 'проектная работа':   # если слово совпадает с ключом
            result = True
        else:
            result = False
        return result

hh_data['проектная работа'] = hh_data['Занятость'].apply(get_project_work)

# Функция для признака "стажировка"
def get_internship(args):
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):                   # Перебираем переданные слова 
        if args_splited[i].strip() == 'стажировка':   # если слово совпадает с ключом
            result = True
        else:
            result = False
        return result

hh_data['стажировка'] = hh_data['Занятость'].apply(get_internship)

# Функция для признака "волонтерство"
def get_volunteering(args):
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):                  # Перебираем переданные слова 
        if args_splited[i].strip() == 'волонтерство':   # если слово совпадает с ключом
            result = True
        else:
            result = False
        return result

hh_data['волонтерство'] = hh_data['Занятость'].apply(get_volunteering)
"""
#Ответ из задания
employments = ['полная занятость', 'частичная занятость',
              'проектная работа', 'волонтерство', 'стажировка']
charts = ['полный день', 'сменный график', 
         'гибкий график', 'удаленная работа',
         'вахтовый метод']
for employment, chart in zip(employments, charts):
    hh_data[employment] = hh_data['Занятость'].apply(lambda x: employment in x)
    hh_data[chart] = hh_data['График'].apply(lambda x: chart in x)

data = hh_data.drop('Занятость', axis=1)
data = hh_data.drop('График', axis=1)


# Сколько людей ищут проектную работу или волонтёрство (в обоих столбцах стоит True)?
#print(hh_data[hh_data['проектная работа'] & hh_data['волонтерство']].shape[0])

# Сколько людей хотят работать вахтовым методом или с гибким графиком (в обоих столбцах стоит True)?
#print(hh_data[hh_data['вахтовый метод'] & hh_data['гибкий график']].shape[0])


df_currency = pd.read_csv('https://www.dropbox.com/s/kik91sgee5jhiz6/ExchangeRates.csv?raw=true', sep=',')
"""В полученной таблице нас будут интересовать столбцы
currency — наименование валюты в ISO-кодировке;
date — дата;
proportion — пропорция;
close — цена закрытия (последний зафиксированный курс валюты на указанный день).
"""

# ВЫДЕЛЕНИЕ АТРИБУТОВ DATETIME
# Тип данных datetime позволяет с помощью специального аксессора dt выделять составляющие времени из каждого элемента столбца, такие как:
# date — дата;
# year, month, day — год, месяц, день;
# time — время;
# hour, minute, second — час, минута, секунда;
# dayofweek — номер дня недели, от 0 до 6, где 0 — понедельник, 6 — воскресенье;
# day_name — название дня недели;
# dayofyear — порядковый день года;
# quarter — квартал (интервал в три месяца).


# 1 Перевести признак «Обновление резюме» из таблицы с резюме в формат datetime и достать из него дату
hh_data['Обновление резюме'] = pd.to_datetime(hh_data['Обновление резюме'])
hh_data['Дата'] = hh_data['Обновление резюме'].dt.date

# В тот же формат привести признак date из таблицы с валютами.
df_currency['date'] = pd.to_datetime(df_currency['date'])

# Выделить из столбца «ЗП» сумму желаемой заработной платы и наименование валюты, в которой она исчисляется. 
def get_salary(args):
    args_splited = args.split(',')
    for i in range(len(args_splited)):
        if args_splited[i].isdigit():
            salary = int(args_splited[i])
        else:
            cur = args_splited[i]
    return salary, cur



# Наименование валюты перевести в стандарт ISO согласно таблице выше.
"""
if __name__ == '__main__':
    experience_col = pd.Series([
        'Опыт работы 8 лет 3 месяца',
        'Опыт работы 3 года 5 месяцев',
        'Опыт работы 1 год 9 месяцев',
        'Опыт работы 3 месяца',
        'Опыт работы 6 лет'
        ])
    experience_month = experience_col.apply(get_experience)
print(experience_month)"""