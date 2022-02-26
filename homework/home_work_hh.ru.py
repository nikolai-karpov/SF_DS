import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


hh_data = pd.read_csv('/Volumes/HDD/Dropbox/Data Science/VS CODE/data/dst-3.0_16_1_hh_database.csv', sep=';')


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
    """[Функция приведения отображения опыта работы к общему показателю в месяцах]

    Args:
        arg ([str]): [На вход получает значение признака 'Опыт работы']

    Returns:
        [int]: [Кол-во месяцев]
    """
    if arg == 'Не указано':
        return np.nan
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

hh_data.drop('Занятость', axis=1)
hh_data.drop('График', axis=1)


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
hh_data['Дата'] = pd.to_datetime(hh_data['Дата'])


# Выделить из столбца «ЗП» сумму желаемой заработной платы 
# и наименование валюты, в которой она исчисляется. 

#Функция выделения валюты
def get_currency(args):
    """[summary]

    Args:
        args ([str]): [сумма и абревиатура валюты]

    Returns:
        [int]: [сумма зарплаты]
    """
    args_splited = args.split(' ')
    currency_salary = None
    for i in range(len(args_splited)):
        if args_splited[i].isalpha():
            currency_salary = args_splited[i]
        return args_splited[1]

hh_data['Валюта'] = hh_data['ЗП'].apply(get_currency)

# Посмотреть кол-во по каждой валюте 
hh_data.groupby(['Валюта']).count()['ЗП']

# Функция отсечения наименования валюты от суммы
def get_salary(args):
    """Функция определения суммы зарплаты

    Args:
        args ([str]): [сумма и абревиатура валюты]

    Returns:
        [int]: [сумма зарплаты]
    """
    args_splited = args.split(' ')
    for i in range(len(args_splited)):
        if args_splited[i].isdigit():
            salary = int(args_splited[i])
        return salary


hh_data['ЗП'] = hh_data['ЗП'].apply(get_salary)


# Скачиваем датасэт с курсами валют
df_currency = pd.read_csv('https://www.dropbox.com/s/kik91sgee5jhiz6/ExchangeRates.csv?raw=true', sep=',')
df_currency['date'] = pd.to_datetime(df_currency['date'])              # Преобразовываем в формат datetime

# Посмотреть курсы валют за день
#     quotes_for_date = df_currency[df_currency['date'] == data].reset_index(drop = True)


def rate_in_date(currency, data):
    """Функция определения курса валюты в запрашиваемый день

    Args:
        currency ([str]): [код валюты ISO]
        data ([datetime]): [дата на которую нужно определить котировку]

    Returns:
        [float]: [курс валюты]
    """
    currency_rate = None
    currency_with_proportion = ['KZT', 'KGS', 'UAH', 'UZS']     # Список валют в которых надо учитывать пропорцию курса
    currency_without_proportion = ['USD', 'EUR', 'BYN', 'AZN']  # Список валют где нет необходимости делить на пропорцию
    mask_date = (df_currency['date'] == data)                   # Маска для фильтрации по дате
    mask_cur = (df_currency['currency'] == currency)            # Маска фильтрации по валюте
    
    if currency == 'RUB':
        currency_rate = 1
    if currency in currency_with_proportion:
        currency_rate = float(df_currency[(mask_date)&(mask_cur)]['close']) \
                / int(df_currency[(mask_date)&(mask_cur)]['proportion'])
                
    if currency in currency_without_proportion:
        currency_rate = float(df_currency[(mask_date)&(mask_cur)]['close'])
    return currency_rate


#df_currency[(df_currency['date'] == data)&(df_currency['currency'] == currency)]['close']
# Получить список валют
list_currencies = df_currency.groupby(df_currency['currency']).mean().reset_index()['currency']

# Наименование валюты перевести в стандарт ISO согласно таблице.
# Cловарь валют для замены
currency_dict = {
    'грн.':	'UAH',
    'USD':	'USD',
    'EUR':	'EUR',
    'бел.руб.':	'BYN',
    'KGS':	'KGS',
    'сум':	'UZS',
    'AZN':	'AZN',
    'KZT':	'KZT',
    'руб.':	'RUB'
}

# Функция замены наименования валюты
hh_data['Валюта'] = hh_data['Валюта'].apply(lambda x: currency_dict[x])


# Привести размер зарплаты к рублю
def get_salary_rub(args):
    """Приведение зарплаты к рублю по курсу банка на дату публикации

    Args:
        args ([str]): [description]

    Returns:
        [int]: [Сумма в рублях по курсу нацбанка]
    """
    sum = int(args[0]) 
    data = args[1] 
    currency = args[2]
    rate = rate_in_date(currency, data)
    
    if currency == 'RUB':
        salary = sum
    else:
        salary = sum*rate # Если валюта не рубль умножаем на курс

    return salary
    
    
hh_data['ЗП (руб)'] = hh_data[['ЗП', 'Дата', 'Валюта']].apply(get_salary_rub, axis=1)


# Чему равна желаемая медианная заработная плата соискателей в нашей таблице (в рублях)? В ответе укажите целое число тысяч.
hh_data['ЗП (руб)'].median()


# Переупорядочил порядок столбцов, чтоб было удобнее работать с данными по ЗП
cols = ['ЗП',
        'ЗП (руб)',
        'Дата',
        'Валюта',
        'Ищет работу на должность:',
        'Город, переезд, командировки',
        'Занятость',
        'График',
        'Последнее/нынешнее место работы',
        'Последняя/нынешняя должность',
        'Обновление резюме',
        'Авто',
        'Образование',
        'Пол',
        'Возраст',
        'Опыт работы (месяц)',
        'Город',
        'Готовность к переезду',
        'Готовность к командировкам',
        'полная занятость',
        'полный день',
        'частичная занятость',
        'сменный график',
        'проектная работа',
        'гибкий график',
        'волонтерство',
        'удаленная работа',
        'стажировка',
        'вахтовый метод']
hh_data = hh_data[cols] 


# чему равна мода распределения
fig = plt.figure('Распределение признака "Возраст"', figsize=figsize3)
fig.subplots_adjust(top=0.8)
fig.suptitle('Распределение признака "Возраст"', fontsize=18)

axes = fig.subplots(1, 2)
ax = axes[0]
ax1 = axes[1]

sns.boxplot(
    ax=ax,
    data=hh_data,
    x='Возраст', 
    orient='h',                   # Горизонтальная расположение
    palette=[colors[0], colors[1]]
)
ax.set_title('Распределение по возрасту', fontsize=14)

# Гистограмма
ages_of_clients = hh_data.groupby('Возраст')['Возраст'].count() # Сортируем и считаем каждую группу по возрасту

sns.histplot(
    ax=ax1,
    data=ages_of_clients,
    x="Возраст"          
)

ax1.set_title('Возрастные группы', fontsize=14)
ax1.set_xlabel('Возраст', fontsize=12)
ax1.set_ylabel('Кол-во чел.', fontsize=12)

plt.show()


# Альтернативное отображение. Но в нем нет кол-ва чел по оси Y
fig = px.histogram(
    data_frame=hh_data,
    x='Возраст',
    title='Распределение возраста соискателей',
    histnorm='percent',
    width=1000,
    marginal='box',
)
fig.show()


# распределение признака "Опыт работы (месяц)"
fig = plt.figure('Распределение признака "Опыт работы (месяц)"', figsize=figsize3)
fig.subplots_adjust(top=0.8)
fig.suptitle('Распределение признака "Опыт работы (месяц)"', fontsize=18)

axes = fig.subplots(1, 2)
ax = axes[0]
ax1 = axes[1]

# Усы
sns.boxplot(
    ax=ax,
    data=hh_data,
    x='Опыт работы (месяц)', 
    orient='h',                   # Горизонтальная расположение
    palette=[colors[0], colors[1]]
)
#ax.set_title('set_title', fontsize=14)
ax.set_xlabel('Опыт в месяцах', fontsize=12)

# Гистограмма
expirience_of_clients = hh_data.groupby('Опыт работы (месяц)')['Опыт работы (месяц)'].count() # Сортируем и считаем каждую группу по возрасту

sns.histplot(
    ax=ax1,
    data=expirience_of_clients,
    x="Опыт работы (месяц)"          
)

#ax1.set_title('set_title', fontsize=14)
ax1.set_xlabel('Опыт в месяцах', fontsize=12)
ax1.set_ylabel('Кол-во чел.', fontsize=12)

plt.show()


# распределение признака "ЗП (руб)"
fig = plt.figure('Распределение признака "ЗП (руб)"', figsize=figsize3)
fig.subplots_adjust(top=0.8)
fig.suptitle('Распределение признака "ЗП (руб)"', fontsize=18)

axes = fig.subplots(1, 2)
ax = axes[0]
ax1 = axes[1]

# Усы
sns.boxplot(
    ax=ax,
    data=hh_data,
    x='ЗП (руб)', 
    orient='h',                   # Горизонтальная расположение
    palette=[colors[0], colors[1]]
)

ax.set_xticklabels([f"{round(x)}млн." for x in ax.get_xticks()/1000000])

# Гистограмма
salary_of_clients = hh_data.groupby(['ЗП (руб)', 'Возраст'])['ЗП (руб)'].count()# Сортируем и считаем каждую группу по возрасту

sns.histplot(
    ax=ax1,
    data=salary_of_clients,
    y='Возраст',
    x="ЗП (руб)"          
)

ax1.set_ylabel('Возраст (лет)', fontsize=12)
ax1.set_xticklabels([f"{round(x)}млн." for x in ax1.get_xticks()/1000000]) # округление по оси X

plt.show()


# Постройте диаграмму, которая показывает зависимость медианной желаемой заработной платы ("ЗП (руб)") от уровня образования ("Образование")
sorted_salary = hh_data[hh_data['ЗП (руб)'] < 1000000]
sorted_salary.groupby('Образование')['ЗП (руб)'].median().plot()


# Постройте диаграмму, которая показывает распределение желаемой заработной платы ("ЗП (руб)") в зависимости от города ("Город")
sorted_salary.groupby('Город')['ЗП (руб)'].median().plot()

fig = px.box(
    sorted_salary,
    y='Город',
    x='ЗП (руб)',
    color='Город',
    title='Распределение желаемой заработной платы в зависимости от города',
    notched=True,
    points="all"
)
fig.show()


# Постройте многоуровневую столбчатую диаграмму, 
# которая показывает зависимость медианной заработной платы ("ЗП (руб)") от признаков 
# "Готовность к переезду" и "Готовность к командировкам"

data_pivot_table = pd.pivot_table(hh_data,
                                  index='Образование',
                                  columns='Возраст',
                                  values='ЗП (руб)',
                                  aggfunc=np.median)

# Тепловая карта  
fig = px.imshow(data_pivot_table)
fig.show()


# Постройте многоуровневую столбчатую диаграмму, которая показывает зависимость медианной заработной платы ("ЗП (руб)") от признаков "Готовность к переезду" и "Готовность к командировкам". 
# Проанализируйте график, сравнив уровень заработной платы в категориях.
data_pivot_table = pd.pivot_table(hh_data,
                                  index=['Готовность к переезду', 'Готовность к командировкам'],
                                  #columns=['ЗП (руб)'],
                                  values=['ЗП (руб)'],
                                  aggfunc=np.median)

"""def moving_business_trip(args):
    result = None
    if args[0] and args[1] == False:
        result = 'Не готов к переезду и командировкам'
    if (args[0] == True) & (args[1] == False):
        result = 'Готов к переезду без командировок'
    if (args[0] == True) & (args[1] == True):
        result = 'Готов к переезду и командировкам'
    if (args[0] == False) & (args[1] == True):
        result = 'Не готов к переезду, но готов к командировкам'
    return result
        

data_pivot_table['Готовность'] = data_pivot_table[['Готовность к переезду', 'Готовность к командировкам']].apply(moving_business_trip, axis=1)
    
    """
  

# Постройте сводную таблицу, иллюстрирующую зависимость медианной желаемой заработной платы от возраста ("Возраст") и образования ("Образование"). На полученной сводной таблице постройте тепловую карту. 
# Проанализируйте тепловую карту, сравнив показатели внутри групп.
data_pivot_table = pd.pivot_table(hh_data,
                                  index='Образование',
                                  columns='Возраст',
                                  values='ЗП (руб)',
                                  aggfunc=np.median)

# Тепловая карта  
fig = px.imshow(data_pivot_table)
fig.show()
    
    
# Постройте диаграмму рассеяния, показывающую зависимость опыта работы ("Опыт работы (месяц)") от возраста ("Возраст").

# Преобразовываем опыт месяцы в года
transformed_expirience = hh_data[['Возраст', 'Опыт работы (месяц)']]
transformed_expirience['Опыт работы (месяц)'] = transformed_expirience['Опыт работы (месяц)'].apply(lambda x: x/12)
transformed_expirience.rename(columns={'Опыт работы (месяц)': 'Опыт работы (лет)'}, inplace=True)                   # Приводим наименование столбца в соответствие содержанию

fig = px.scatter(
    transformed_expirience, 
    x='Возраст', 
    y='Опыт работы (лет)'
)

# построить прямую для выявления аномалии
fig.add_trace(go.Scatter(x=[0, 100], y=[0, 100],
                    mode='lines',
                    name='Возраст=Стаж'))

fig.show()


# Очистка данных

# Найдите полные дубликаты в таблице с резюме и удалите их
duplicates = hh_data[hh_data.duplicated(subset=hh_data.columns)]
print('Число дубликтов: {}'.format(duplicates.shape[0]))

hh_data = hh_data.drop_duplicates()
print('В результате осталось после очистки записей: {}'.format(hh_data.shape[0]))

# Выведите информацию о числе пропусков в столбцах
cols_nan_percent = hh_data.isna().sum()
cols_with_nan = cols_nan_percent[cols_nan_percent > 0].sort_values(ascending=False)
cols_with_nan

#hh_data[hh_data['Опыт работы (месяц)'].isna() == True].reset_index()
#null_data = hh_data.isnull().sum()
#display(null_data[null_data > 0])


# удалите строки, где есть пропуск в столбцах с местом работы и должностью. 
# Пропуски в столбце с опытом работы заполните медианным значением

# Создаю копию данных
hh_data_copy = hh_data.copy()

# Удаляю строчки с NaN из столбцов "Последнее/нынешнее место работы" и "Последняя/нынешняя должность"
#hh_data_copy = hh_data_copy[~((hh_data_copy['Последнее/нынешнее место работы'].isna()) | 
#                  (hh_data_copy['Последняя/нынешняя должность'].isna())
#                  )]
hh_data_copy = hh_data_copy.dropna(subset=['Последнее/нынешнее место работы', 'Последняя/нынешняя должность'])

print(f'Найдено {hh_data_copy["Опыт работы (месяц)"].isna().sum()} NAN значений')

# Заполняю NaN медианными значениями
#hh_data_copy = hh_data_copy.fillna(value={'Опыт работы (месяц)': hh_data_copy['Опыт работы (месяц)'].median()})
hh_data_copy['Опыт работы (месяц)'] = hh_data_copy['Опыт работы (месяц)'].fillna(hh_data_copy['Опыт работы (месяц)'].median())

print(f'Осталось {hh_data_copy["Опыт работы (месяц)"].isna().sum()} NAN значений.')
print('Результирующее среднее значение Опыт работы (месяц)', round(hh_data_copy['Опыт работы (месяц)'].mean(),0))

# Заменяю данных на очищенные
hh_data = hh_data_copy.copy()

# Альтернативный способ
# Удаляю строчки с NaN
hh_data = hh_data.dropna(subset=['Последнее/нынешнее место работы', 'Последняя/нынешняя должность'])
print(f'Найдено {hh_data["Опыт работы (месяц)"].isna().sum()} NAN значений')

hh_data = hh_data.fillna(
    value={'Опыт работы (месяц)': hh_data['Опыт работы (месяц)'].median()}
    )

hh_data['Опыт работы (месяц)'] = hh_data['Опыт работы (месяц)'].fillna(
    hh_data['Опыт работы (месяц)'].median()
    )


# Удалите резюме, в которых указана заработная плата либо выше 1 млн. рублей, либо ниже 1 тыс. рублей.
# Сколько выбросов
# Cколько соискателей ищут заработную плату выше 1 миллиона рублей.
above_million = hh_data[hh_data['ЗП (руб)'] > 1000000].reset_index().count()
print(f'Зарплата свыше 1 млн руб. заявлена у {above_million[1]} чел.')

# Cколько соискателей указали желаемую зарплату ниже 1 тыс.рублей.
below_thousand = hh_data[hh_data['ЗП (руб)'] < 1000].reset_index().count()
print(f'Зарплата ниже 1 тыс.руб. заявлена у {below_thousand[1]} чел.')

# Удалите резюме, в которых указана заработная плата либо выше 1 млн
#hh_data = hh_data[~(hh_data['ЗП (руб)'] > 1000000)]

# Удалите резюме, в которых указана заработная плата ниже 1 тыс. рублей
#hh_data = hh_data[~(hh_data['ЗП (руб)'] < 1000)]

outliers = hh_data[(hh_data['ЗП (руб)'] > 1e6) | (hh_data['ЗП (руб)'] < 1e3)]
hh_data = hh_data.drop(outliers.index)
print('Удалено: ', outliers.shape[0])


# Найдите резюме в которых опыт работы в годах превышал возраст соискателя и удалите их из данных
# Cколько соискателей имеют опыт превышающий их возраст
experience_exceeds_age = hh_data[(hh_data['Опыт работы (месяц)']/12) >= hh_data['Возраст']].reset_index().count()
print(f'Опыт превышает возраст у {experience_exceeds_age[1]} чел.')

# Удалите резюме, в которых опыт превышает возраст
#hh_data = hh_data[~((hh_data['Опыт работы (месяц)']/12) >= hh_data['Возраст'])]
outliers = hh_data[hh_data['Опыт работы (месяц)']/12 >= hh_data['Возраст']]
hh_data = hh_data.drop(outliers.index)
print('Удалено: ', outliers.shape[0])  


# построить распределение признака в логарифмическом масштабе. 
# Добавьте к графику линии, отображающие среднее и границы интервала метода трех сигм
#  построить распределение признака в логарифмическом масштабе
fig, ax = plt.subplots(1, 1, figsize=(8, 4))
log_age = np.log(hh_data['Возраст'] + 1)
histplot = sns.histplot(log_age, bins=30, ax=ax)
histplot.axvline(log_age.mean(), color='k', lw=2)
histplot.axvline(log_age.mean()+4*log_age.std(), color='k', ls='--', lw=2)
histplot.axvline(log_age.mean()-3*log_age.std(), color='k', ls='--', lw=2)
histplot.set_title('логарифмическое распределение');

plt.show()

# Найдите выбросы с помощью метода z-отклонения
def outliers_z_score(data, feature, left=3, right=3, log_scale=False):
    """Функция поиска выбросов с помощью метода z-отклонения 

    Args:
        data (DataFrame): Датасет в котором будут анализироваться выбросы
        feature (str): Данные признака по которому анализируются выбросы
        left (int, optional): Колличество сигм левой границы интервала. Defaults to 3.
        right (int, optional): Колличество сигм правой границы интервала. Defaults to 3.
        log_scale (bool, optional): _description_. Defaults to False.

    Returns:
        DataFrame:  outliers - Число выбросов по методу z-отклонения
                    cleaned - очищенный датасет
    """
    if log_scale:
        x = np.log(data[feature]+1)
    else:
        x = data[feature]
    mu = x.mean()
    sigma = x.std()
    lower_bound = mu - left * sigma
    upper_bound = mu + right * sigma
    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x > lower_bound) & (x < upper_bound)]
    return outliers, cleaned


outliers, cleaned = outliers_z_score(hh_data, 'Возраст', left=3,  right=4, log_scale=False)
print(f'Число выбросов по методу z-отклонения: {outliers.shape[0]}')
print(f'Результирующее число записей: {cleaned.shape[0]}')