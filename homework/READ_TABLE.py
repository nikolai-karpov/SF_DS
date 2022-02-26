import pandas as pd

countries_data = pd.read_csv('homework/data/countries.csv', sep=';')         # Загружаем данные из файла в переменную, создавая объект DataFrame
countries_data.to_csv('homework/data/countries.txt', index=False, sep=' ')   # Выгружаем данные из DataFrame в CSV-файл и сохраняем файл в папке data

txt_df = pd.read_table('homework/data/countries.txt', 
                       sep=' ', index_col=['country'])                       # Загружаем данные из файла в переменную, создавая объект DataFrame
#print(txt_df)                                                                # Выводим содержимое DataFrame на экран


# ЛОКАЛИЗУЕМ ПРОБЛЕМУ
# Считываем файл и создаем DataFrame без использования параметра encoding
#data=pd.read_csv('homework/data/ErrorEnCoding.csv', 
 #                header=None)            # Считываем данные из файла с неизвестной кодировкой в переменную, создавая объект DataFrame


# ОПРЕДЕЛЯЕМ КОДИРОВКУ ФАЙЛА
from chardet.universaldetector import UniversalDetector # Импортируем субмодуль chardet.universaldetector

detector = UniversalDetector()
with open('homework/data/ErrorEnCoding.csv', 'rb') as fh:
    for line in fh:
        detector.feed(line)
        if detector.done:
            break

#print(detector.close())


# СЧИТЫВАЕМ ФАЙЛ, УКАЗАВ КОДИРОВКУ

data=pd.read_csv('homework/data/ErrorEnCoding.csv', 
                 encoding='koi8-r', 
                 header=None
                 )# Создаем DataFrame из файла, явно указав кодировку символов, и выводим его содержимое на экран


# ЧТЕНИЕ ФАЙЛА ПО ССЫЛКЕ, ИСПОЛЬЗУЯ ФУНКЦИЮ READ_TABLE()
data = pd.read_table('https://raw.githubusercontent.com/esabunor/MLWorkspace/master/melb_data.csv', sep=',')


# ЧТЕНИЕ/ЗАПИСЬ АРХИВИРОВАННЫХ CSV-ФАЙЛОВ
data = pd.read_csv('homework/data/students_performance.zip')


# УПАКОВКА CSV-файлов в zip-архив
# Определяем параметры архивирования — метод сжатия, имя файл в архиве
compression_opts = dict(
    method='zip', 
    archive_name='out.csv') 

data.to_csv('homework/data/out.zip', 
            index=False, 
            compression=compression_opts)

#print(data)                              # Выводим содержимое DataFrame на экран