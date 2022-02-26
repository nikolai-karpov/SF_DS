import pandas as pd

# Основные параметры метода read_excel()
"""
io 
— первый параметр, в который мы передаём адрес файла, который хотим прочитать. Кроме адреса на диске, можно передавать адрес в интернете.

sheet_name 
—  ссылка на лист в Excel-файле (возможные значения данного параметра: 0 — значение по умолчанию, загружается первый лист; 
'Sheet1' — можно передать название листа; 
обычно листы называются 'SheetX', где X — номер листа, но могут использоваться и другие названия; 
[0, 1, 'Sheet3'] — список, содержащий номера или названия листов; 
в таком случае Pandas вернёт словарь, в котором ключами будут номера или названия листов, а значениями — их содержимое в виде DataFrame; 
None — если передать такое значение, то pandas прочитает все листы и вернёт их в виде словаря, как в предыдущем пункте).

na_values 
— список значений, которые будут считаться пропусками ( ‘’, ‘#N/A’, ‘ N/A’, ‘#NA’, ‘-1.#IND’, ‘-1.#QNAN’, ‘-NaN’, ‘-nan’, ‘1.#IND’, ‘1.#QNAN’, ‘NA’, ‘NULL’, ‘NaN’, ‘n/a’, ‘nan’, ‘null’).
"""
# По умолчанию в DataFrame читается информация из первого листа
#grades = pd.read_excel('homework/data/grades.xlsx')


# СЧИТЫВАНИЕ ДАННЫХ ИЗ ФАЙЛА EXCEL ПО ССЫЛКЕ
#data = pd.read_excel('https://github.com/asaydn/test/raw/master/january.xlsx')


# Чтобы прочесть данные из следующих листов кроме первого указываем имя листа
#grades = pd.read_excel('homework/data/grades.xlsx', sheet_name='Maths')


# ВЫГРУЗКА ДАННЫХ ИЗ DATAFRAME В EXCEL-ФАЙЛ
#grades.to_excel('homework/data/grades_new.xlsx') # Сохраняем данные из DataFrame grades в файл grades_new.xlsx в папке data
# В этом случае будет создан один лист с именем по умолчанию "Sheet1". 
# Также в данных будет находиться лишний столбец с индексами!


# Сохраняем данные из DataFrame grades в файл grades_new.xlsx (на листе 'Example') в папке data
#grades.to_excel('homework/data/grades_new.xlsx', sheet_name='Example', index=False) 


# Продвинутая работа с файлами Excel
"""
openpyxl — рекомендуемый пакет для чтения и записи файлов Excel 2010+ (например, xlsx);
xlsxwriter — альтернативный пакет для записи данных, информации о форматировании и, в частности, диаграмм в формате Excel 2010+ (например, xlsx);
pyxlsb — пакет позволяет читать файлы Excel в xlsb-формате;
pylightxl — пакет позволяет читать xlsx- и xlsm-файлы и записывать xlsx-файлы;
xlrd — пакет предназначен для чтения данных и информации о форматировании из старых файлов Excel (например, xls);
xlwt — пакет предназначен для записи данных и информации о форматировании в старые файлы Excel (например, xls). 
"""


# Считайте данные из двух листов файла ratings+movies.xlsx в разные DataFrame
ratings = pd.read_excel('homework/data/ratings+movies.xlsx', sheet_name='ratings')
movies = pd.read_excel('homework/data/ratings+movies.xlsx', sheet_name='movies')

# объедините в один
# МЕТОД ОБЪЕДИНЕНИЯ JOIN
joined = ratings.join(          # Чтобы совместить таблицы по ключевому столбцу с помощью метода join()
    movies.set_index('movieId'),# необходимо использовать ключевой столбец в «правой» таблице в качестве индекса
    on='movieId',               # необходимо указать название ключа в параметре on.
    how='left'
)


# МЕТОД ОБЪЕДИНЕНИЯ MERGE
# Произведём слияние наших таблиц и получим ту же таблицу, что и ранее:
merged = ratings.merge(
    movies,
    on='movieId',
    how='left'
)

# Запишите данные из полученного DataFrame в файл
joined.to_excel('joined.xlsx', sheet_name='JOINED', index=False)
