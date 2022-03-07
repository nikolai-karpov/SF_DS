import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Параметры общего стиля
#sns.set_style("whitegrid")
colors = sns.color_palette("pastel")
figsize = (6, 4)    # Для одного фрейма
figsize2 = (12, 4)  # Для двух фреймов
figsize3 = (16, 4)  # Для трёх фреймов


hh_data = pd.read_csv('/Volumes/HDD/Dropbox/Data Science/VS CODE/data/dst-3.0_16_1_hh_database.csv', sep=';')

# Преобразование данных

def get_education(arg):
    """[Функция преобразования признака Образование и ВУЗ]

    Args:
        args ([str]): [На вход получает содержание признака 'Образование и ВУЗ']

    Returns:
        [str]: [Возвращает категорию образования]
    """
    arg = ' '.join(arg.split(' ')[:3])
    if 'Высшее' in arg:
        return 'высшее'
    elif 'Неоконченное высшее' in arg:
        return 'неоконченное высшее'
    elif 'Среднее специальное' in arg:
        return 'среднее специальное'
    elif 'Среднее образование' in arg:
        return 'среднее'

# Создаем признак "Образование"        
hh_data['Образование'] = hh_data['Образование и ВУЗ'].apply(get_education)

# Удаляем ненужны столбец
hh_data = hh_data.drop('Образование и ВУЗ', axis=1)                         

# Выделяем категориальные признаки
hh_data['Образование'] = hh_data['Образование'].astype('category')                        


# Сколько соискателей имеет средний уровень образования (школьное образование)?
#print(hh_data['Образование'].value_counts(dropna=False))


# Создайте признак "Пол" 
# Признак пола должен иметь 2 уникальных строковых значения: 'М' - мужчина, 'Ж' - женщина.
# Создайте признак "Возраст".
# Признак возраста должен быть представлен целыми числами.
def get_gender(args):
    """[Фнкция преобразавания признака Пол]

    Args:
        args ([str]): [Пол, возраст, дату рождения]

    Returns:
        [str]: [2 уникальных строковых значения: 'М' - мужчина, 'Ж' - женщина.]
    """
    if 'Мужчина ' in args:
        return 'М'
    if 'Женщина ' in args:
        return 'Ж'


def get_age(arg):
    """[Фнкция преобразавания признака ВОЗРАСТ]

    Args:
        args ([str]): [Пол, возраст]

    Returns:
        [str]: [Возраст]
    """
    arg_splitted = arg.split(' ')
    year_words=['год', 'года', 'лет']
    for index, item in enumerate (arg_splitted):
        if item in year_words:
            return int(arg_splitted[index-1])

            
hh_data['Пол'] = hh_data['Пол, возраст'].apply(get_gender)

hh_data['Возраст'] = hh_data['Пол, возраст'].apply(get_age) 

# Преобразуем данные для оптимизации памяти
hh_data['Возраст'] = hh_data['Возраст'].astype(np.int64)  

#percentage_women = hh_data.groupby('Пол')['Пол'].count().transform(lambda x: x / hh_data.shape[0] * 100)
#print(f"Женских резюме {round(hh_data['Пол'].value_counts(normalize=True)['Ж'] * 100, 2)} %")
#print('Средний возраст соискателей', round(hh_data['Возраст'].mean(), 1))

# Удаляем ненужный признак
hh_data = hh_data.drop('Пол, возраст', axis=1)

 
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
    if arg is np.nan or arg == 'Не указано':
        return None                       # Возвращаем None чтоб не бло ошибок при построении графиков

    # Задаем ключевые слова для сравнения
    year_words=['год', 'года', 'лет']
    month_words=['месяц', 'месяца', 'месяцев']

    arg_splitted = arg.split(' ')[:7]
    
    # Создаем счетчики
    years = 0
    months = 0

    for index, item in enumerate (arg_splitted):
        if item in year_words:
            years = int(arg_splitted[index-1])
        if item in month_words:
            months = int(arg_splitted[index-1])
    return int(years*12 + months)


hh_data['Опыт работы (месяц)'] = hh_data['Опыт работы'].apply(get_experience)
hh_data = hh_data.drop('Опыт работы', axis=1)

# Чему равен медианный опыт работы (в месяцах) в нашей таблице?
#print('Медианный опыт работы (в месяцах) равен', round(hh_data['Опыт работы (месяц)'].median()))


# Создадим отдельные признаки 
# «Город»
# Список городов-миллионников:
million_cities = ['Новосибирск', 'Екатеринбург', 'Нижний Новгород', 'Казань', 'Челябинск', 'Омск', 'Самара', 'Ростов-на-Дону', 'Уфа', 'Красноярск', 'Пермь', 'Воронеж', 'Волгоград' ]


def get_citi(args):
    """[Функция определения категории города]

    Args:
        args ([str]): [Город, переезд, командировки]

    Returns:
        [str]: [Возвращает 4 категории: "Москва", "Санкт-Петербург" и "город-миллионник" и "другие" ]
    """
    city = args.split(' , ')[0]
    if (city == 'Москва') or (city == 'Санкт-Петербург'):
        return city
    elif city in million_cities:
        return 'город миллионник'
    else:
        return 'другие'


hh_data['Город'] = hh_data['Город, переезд, командировки'].apply(get_citi)

# Сколько процентов соискателей живут в Санкт-Петербурге?
urban_residents = hh_data.groupby('Город')['Город'].count().transform(lambda x: x / hh_data.shape[0] * 100)
print(round(urban_residents[1]), '% соискателей живут в Санкт-Петербурге')


def ready_to_move(args):
    """[Функция формирования данных для признака Готовность к переезду]

    Args:
        args ([str]): [Город, переезд, командировки]

    Returns:
        [bool]: [готов = True, не готов = False]
    """
    result = None
    if ('не готов к переезду' in args) or ('не готова к переезду' in args) or ('не хочу переезжать' in args):
        result = False  
    elif 'хочу' in args:
        return True
    else:
        result = True
    return result


hh_data['Готовность к переезду'] = hh_data['Город, переезд, командировки'].apply(ready_to_move)

# Сколько процентов соискателей готовы к переездам?
percent_to_move = hh_data.groupby('Готовность к переезду')['Готовность к переезду'].count().transform(lambda x: x / hh_data.shape[0] * 100)
print(round(percent_to_move[1]), '% соискателей готовы к переездам')


def ready_business_trip(args):
    """[Функция определения данных для признака Готовность к командировкам]

    Args:
        args ([str]): [Город, переезд, командировки]

    Returns:
        [bool]: [готов = True, не готов = False]
    """
    list_variants = ['готов к командировкам', 'готова к командировкам', 'готов к редким командировкам', 'готова к редким командировкам']
    args_splited = args.split(',')
    result = None
    for i in range(len(args_splited)):                 # Перебираем переданные слова 
        if args_splited[i].strip() in list_variants:   # если слово совпадает с ключом
            result = True
        else:
            result = False
    return result


hh_data['Готовность к командировкам'] = hh_data['Город, переезд, командировки'].apply(ready_business_trip)
hh_data = hh_data.drop('Город, переезд, командировки', axis=1)

# Выделяем категориальные признаки
hh_data['Город'] = hh_data['Город'].astype('category')

# Сколько процентов соискателей готовы одновременно и к переездам, и к командировкам?
percent_business_trip = round(hh_data[hh_data['Готовность к переезду'] & hh_data['Готовность к командировкам']].shape[0] / hh_data.shape[0] *100)
#print(round(percent_business_trip), '% соискателей готовы одновременно и к переездам, и к командировкам')


# Преобразование для признаков «Занятость» и «График»

"""Все что я насочинял собирает данные которые не принимает курс
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


def get_salary(args):
    """Функция отсечения наименования валюты от суммы

    Args:
        args ([str]): [сумма и абревиатура валюты]

    Returns:
        [int]: [сумма зарплаты]
    """
    salary = float(args.split(' ')[0])
    return salary



def get_salary_currency(arg):
    """Функция приведения наименования валюты к стандарту ISO

    Args:
        args ([str]): [сумма и валюта в которой зарплата]

    Returns:
        [str]: [код валюты в стандарте ISO]
    """  
    currency_dict = {
        'USD': 'USD', 'KZT': 'KZT',
        'грн': 'UAH', 'белруб': 'BYN',
        'EUR': 'EUR', 'KGS': 'KGS',
        'сум': 'UZS', 'AZN': 'AZN'
    }
    curr = arg.split(' ')[1].replace('.', '')
    if curr == 'руб':
        return 'RUB'
    else:
        return currency_dict[curr]


# Формирование датасета с курсами валют
rates = pd.read_csv('https://www.dropbox.com/s/kik91sgee5jhiz6/ExchangeRates.csv?raw=true', sep=',')
# Преобразовываем в формат datetime
rates['date'] = pd.to_datetime(rates['date'], dayfirst=True).dt.date 

# Перевести признак «Обновление резюме» из таблицы с резюме в формат datetime и достать из него дату
hh_data['Обновление резюме'] = pd.to_datetime(hh_data['Обновление резюме'], dayfirst=True).dt.date

# Создаем временный признак для зарплаты
hh_data['ЗП (tmp)'] = hh_data['ЗП'].apply(get_salary)

# Создаем временный признак и заполняем его наименованием валюты по ISO
hh_data['ISO (tmp)'] = hh_data['ЗП'].apply(get_salary_currency)

# Объединяем датасеты ориентируясь на дату и наименование валюты
merged = hh_data.merge(
    rates, 
    left_on=['ISO (tmp)', 'Обновление резюме'],
    right_on=['currency', 'date',], 
    how='left'
)

# Заполняем единицей ячейки столбца с курсом, там где есть пропуски данных
merged['close'] = merged['close'].fillna(1)

# Заполняем единицей ячейки столбца с пропорцией там где пропуски 
merged['proportion'] = merged['proportion'].fillna(1)

# Создаем признак зарплата в рублях
hh_data['ЗП (руб)'] = merged['close'] * merged['ЗП (tmp)'] / merged['proportion']

# Удаляем ненужные признаки
hh_data = hh_data.drop(['ЗП', 'ЗП (tmp)', 'ISO (tmp)'], axis=1)

# Отвечаем на вопрос в задании
# Чему равна желаемая медианная заработная плата соискателей в нашей таблице (в рублях)?
#print(f"Медианная заработная плата соискателей равна {round(hh_data['ЗП (руб)'].median()/1000)} руб")


# Исследование зависимостей в данных

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


# Чему равна мода распределения
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
    data=hh_data,
    x="Возраст"          
)

ax1.set_title('Возрастные группы', fontsize=14)
ax1.set_xlabel('Возраст', fontsize=12)
ax1.set_ylabel('Кол-во чел.', fontsize=12)

plt.show()


# Распределение признака "Опыт работы (месяц)"
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

ax.set_xlabel('Опыт в месяцах', fontsize=12)

# Гистограмма
expirience_of_clients = hh_data.groupby('Опыт работы (месяц)')['Опыт работы (месяц)'].count() # Сортируем и считаем каждую группу по возрасту

sns.histplot(
    ax=ax1,
    data=hh_data,
    x="Опыт работы (месяц)"          
)

#ax1.set_title('set_title', fontsize=14)
ax1.set_xlabel('Опыт в месяцах', fontsize=12)
ax1.set_ylabel('Кол-во чел.', fontsize=12)

plt.show()

# Чему равен максимальный опыт работы (в месяцах)?
#print(f"максимальный опыт работы равен {round(hh_data['Опыт работы (месяц)'].max())} мес.")


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

ax.set_xticklabels([f"{x}млн." for x in ax.get_xticks()/1000000])

# Гистограмма
salary_of_clients = hh_data.groupby(['ЗП (руб)', 'Возраст'])['ЗП (руб)'].count()# Сортируем и считаем каждую группу по возрасту

sns.histplot(
    ax=ax1,
    data=hh_data,
    y='Возраст',
    x="ЗП (руб)"          
)

ax1.set_ylabel('Возраст (лет)', fontsize=12)
ax1.set_xticklabels([f"{x}млн." for x in ax1.get_xticks()/1000000]) # округление по оси X

plt.show()


# Ответ на задание модуля
above_million = hh_data[hh_data['ЗП (руб)'] > 1000000].reset_index().count()
#print(above_million[1],' соискателей требуют заработную плату выше 1 миллиона рублей')


# Постройте диаграмму, которая показывает зависимость медианной желаемой заработной платы ("ЗП (руб)") от уровня образования ("Образование")
sorted_salary = hh_data[hh_data['ЗП (руб)'] < 1000000]
sorted_salary.groupby('Образование')['ЗП (руб)'].median().plot()

# Альтернативный график
bar_data = hh_data[hh_data['ЗП (руб)']<1e6].groupby('Образование', as_index=False).median()
fig = px.bar(
    data_frame=bar_data,
    x='Образование',
    y='ЗП (руб)',
    title='Медианная з/п по уровню образования',
    color='Образование'
)
fig.show()


# Постройте диаграмму, которая показывает распределение желаемой заработной платы ("ЗП (руб)") в зависимости от города ("Город")
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
bar_data = hh_data.groupby(
    ['Готовность к командировкам', 'Готовность к переезду'],
    as_index=False
)['ЗП (руб)'].median()

fig = px.bar(
    data_frame=bar_data,
    y='Готовность к переезду',
    x='ЗП (руб)',
    barmode="group",
    color='Готовность к командировкам',
    orientation='h',
    title='Медианная з/п по готовности к командировкам/переезду'
)
fig.show()

# Альтернативный график для Github
hh_data.groupby(['Готовность к переезду', 'Готовность к командировкам'])['ЗП (руб)'].median().plot()


# Постройте сводную таблицу, иллюстрирующую зависимость медианной желаемой заработной платы от возраста ("Возраст") и образования ("Образование"). На полученной сводной таблице постройте тепловую карту. 
# Проанализируйте тепловую карту, сравнив показатели внутри групп.
data_pivot_table = pd.pivot_table(hh_data,
                                  index='Образование',
                                  columns='Возраст',
                                  values='ЗП (руб)',
                                  aggfunc=np.median,
                                  fill_value=0)

# Тепловая карта  
fig = px.imshow(data_pivot_table, aspect='auto', title='Медианная з/п по образованию и возрасту')
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


# ДОПОЛНИТЕЛЬНЫЕ ГРАФИКИ

# Медианная з/п по образованию и Городу
data_pivot_table = pd.pivot_table(hh_data,
                                  index='Образование',
                                  columns='Город',
                                  values='ЗП (руб)',
                                  aggfunc=np.median,
                                  fill_value=0)

# Тепловая карта  
fig = px.imshow(data_pivot_table, aspect='auto', title='Медианная з/п по образованию и Городу')
fig.show()

# Зависимость готовности  к переезду и командировкам от возраста
bar_data = hh_data.groupby(
    ['Готовность к командировкам', 'Готовность к переезду'],
    as_index=False
)['Возраст'].mean()

fig = px.bar(
    data_frame=bar_data,
    y='Готовность к переезду',
    x='Возраст',
    barmode="group",
    color='Готовность к командировкам',
    orientation='h',
    title='Зависимость готовности  к переезду и командировкам от возраста'
)
fig.show()

# Зависмость Образование и Возраст
fig = px.histogram(
    data_frame=hh_data,
    x='Возраст',
    y='Образование',
    histfunc='avg',
    color='Образование',
    title='Зависмость Образование и Возраст'
)
fig.show()

# Зависмость уровня образования и готовности к командировкам и переезду
bar_data = hh_data.groupby(['Образование'],as_index=False)['Готовность к командировкам', 'Готовность к переезду'].count()

fig = px.histogram(
    bar_data, 
    x='Образование', 
    y=['Готовность к командировкам', 'Готовность к переезду'], 
    title='Зависмость уровня образования и готовности к командировкам и переезду',
    histnorm='probability density'
    )

fig.show()


# Очистка данных

# Найдите полные дубликаты в таблице с резюме и удалите их
# Определяем дубликаты
duplicates = hh_data[hh_data.duplicated(subset=hh_data.columns)]
#print('Число дубликтов: {}'.format(duplicates.shape[0]))

hh_data = hh_data.drop_duplicates()
#print('В результате осталось после очистки записей: {}'.format(hh_data.shape[0]))

# Определяем долю пропусков 
cols_nan_percent = hh_data.isna().sum()
cols_with_nan = cols_nan_percent[cols_nan_percent > 0].sort_values(ascending=False)

# и выводим результат 
cols_with_nan

# Альтернативный вариант
#hh_data[hh_data['Опыт работы (месяц)'].isna() == True].reset_index()
#null_data = hh_data.isnull().sum()
#display(null_data[null_data > 0])


# Создаю копию данных
hh_data_copy = hh_data.copy()

# Удаляю строчки с NaN из столбцов "Последнее/нынешнее место работы" и "Последняя/нынешняя должность"
hh_data = hh_data[~((hh_data['Последнее/нынешнее место работы'].isna()) | 
                  (hh_data['Последняя/нынешняя должность'].isna())
                  )]



# Заменяю данных на очищенные
#hh_data = hh_data_copy.copy()

# Альтернативный способ
# Удаляю строчки с NaN
hh_data = hh_data.dropna(subset=['Последнее/нынешнее место работы', 'Последняя/нынешняя должность'])
#print(f'Найдено {hh_data["Опыт работы (месяц)"].isna().sum()} NAN значений')

# Заполняю NaN медианными значениям
hh_data = hh_data.fillna(
    value={'Опыт работы (месяц)': hh_data['Опыт работы (месяц)'].median()}
    )

hh_data['Опыт работы (месяц)'] = hh_data['Опыт работы (месяц)'].fillna(
    hh_data['Опыт работы (месяц)'].median()
    )

# Альтернативный вариант заполнения NaN медианными значениями
#hh_data_copy = hh_data_copy.fillna(value={'Опыт работы (месяц)': hh_data_copy['Опыт работы (месяц)'].median()})
#hh_data_copy['Опыт работы (месяц)'] = hh_data_copy['Опыт работы (месяц)'].fillna(hh_data_copy['Опыт работы (месяц)'].median())

#print(f'Осталось {hh_data_copy["Опыт работы (месяц)"].isna().sum()} NAN значений.')
#print('Результирующее среднее значение Опыт работы (месяц)', round(hh_data_copy['Опыт работы (месяц)'].mean(),0))


# Удалите резюме, в которых указана заработная плата либо выше 1 млн. рублей, либо ниже 1 тыс. рублей.
# Сколько выбросов
# Сортировка соискателей ищущих заработную плату выше 1 миллиона рублей.
above_million = hh_data[hh_data['ЗП (руб)'] > 1000000].reset_index().count()
#print(f'Зарплата свыше 1 млн руб. заявлена у {above_million[1]} чел.')

# Cколько соискателей указали желаемую зарплату ниже 1 тыс.рублей.
below_thousand = hh_data[hh_data['ЗП (руб)'] < 1000].reset_index().count()
#print(f'Зарплата ниже 1 тыс.руб. заявлена у {below_thousand[1]} чел.')

# Удалите резюме, в которых указана заработная плата либо выше 1 млн
#hh_data = hh_data[~(hh_data['ЗП (руб)'] > 1000000)]

# Удалите резюме, в которых указана заработная плата ниже 1 тыс. рублей
#hh_data = hh_data[~(hh_data['ЗП (руб)'] < 1000)]

# Альтернативное решение
outliers = hh_data[(hh_data['ЗП (руб)'] > 1e6) | (hh_data['ЗП (руб)'] < 1e3)]
hh_data = hh_data.drop(outliers.index)
#print('Удалено: ', outliers.shape[0])


# Найдите резюме в которых опыт работы в годах превышал возраст соискателя и удалите их из данных
# Cколько соискателей имеют опыт превышающий их возраст
experience_exceeds_age = hh_data[(hh_data['Опыт работы (месяц)']/12) >= hh_data['Возраст']].reset_index().count()
#print(f'Опыт превышает возраст у {experience_exceeds_age[1]} чел.')

# Удаление резюме, в которых опыт превышает возраст
outliers = hh_data[hh_data['Опыт работы (месяц)']/12 >= hh_data['Возраст']]
hh_data = hh_data.drop(outliers.index)
#print('Удалено: ', outliers.shape[0])     

# Альтернативный вариант
#hh_data = hh_data[~((hh_data['Опыт работы (месяц)']/12) >= hh_data['Возраст'])]


# построить распределение признака в логарифмическом масштабе. 
# Добавьте к графику линии, отображающие среднее и границы интервала метода трех сигм
# Построение графика распределение признака в логарифмическом масштабе
fig, ax = plt.subplots(1, 1, figsize=(8, 4))
log_age = np.log(hh_data['Возраст'] + 1)
histplot = sns.histplot(log_age, bins=30, ax=ax)
histplot.axvline(log_age.mean(), color='k', lw=2)
histplot.axvline(log_age.mean()+4*log_age.std(), color='k', ls='--', lw=2)
histplot.axvline(log_age.mean()-3*log_age.std(), color='k', ls='--', lw=2)
histplot.set_title('логарифмическое распределение');

ax.set_xticklabels([round(x) for x in ax.get_xticks()**3])

plt.show()

# Поиск выбросов с помощью метода z-отклонения
def outliers_z_score(data, feature, left=3, right=3, log_scale=False):
    """Функция поиска выбросов с помощью метода z-отклонения 

    Args:
        data (DataFrame): Датасет в котором будут анализироваться выбросы
        feature (str): Данные признака по которому анализируются выбросы
        left (int, optional): Колличество сигм левой границы интервала. Defaults to 3.
        right (int, optional): Колличество сигм правой границы интервала. Defaults to 3.
        log_scale (bool, optional): Если True тогда в расчете мю и сигмы используется np.log. Defaults to False.

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

    lower_bound = mu - (left * sigma)
    upper_bound = mu + (right * sigma)

    outliers = data[(x < lower_bound) | (x > upper_bound)]
    cleaned = data[(x > lower_bound) & (x < upper_bound)]

    return outliers, cleaned

# Применение функции и вывод результатов
outliers, cleaned = outliers_z_score(hh_data, 'Возраст', left=3,  right=4, log_scale=True)
print(f'Число выбросов по методу z-отклонения: {outliers.shape[0]}')
print(f'Результирующее число записей: {cleaned.shape[0]}')