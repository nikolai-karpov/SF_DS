import requests                 # Импортируем библиотеку requests
from bs4 import BeautifulSoup   # Импортируем библиотеку BeautifulSoup
from pprint import pprint       # Импортируем функцию pprint()
import time                     # Импортируем модуль time


token = 'c22b3e0bc22b3e0bc22b3e0b0ec250afc0cc22bc22b3e0ba001682b457a61bc5e48e073'


# СБОР ИНФОРМАЦИИ ИЗ ГРУПП
url = 'https://api.vk.com/method/groups.getMembers' # Указываем адрес обращения

# Формируем строку параметров
params = {'group_id': 'dwgformat', 
          'v': 5.95, 
          'access_token': token
          } 
response = requests.get(url, params = params)   # Посылаем запрос
data = response.json()                          # Ответ сохраняем в переменной data в формате слова
# count - общее число участников группы
# items - id участников группы


# Выгружаем id пользователей партиями по count за раз
count = 1000 
offset = 0 
user_ids = [] 
max_count = data['response']['count'] 
while offset < max_count: 
    # Будем выгружать по count=<кол-во> пользователей, 
    # начиная с того места, где закончили на предыдущей итерации (offset) 
    print('Выгружаю {} пользователей с offset = {}'.format(count, offset))   
    params = {'group_id': 'dwgformat', 
              'v': 5.95, 
              'count': count, 
              'offset': offset, 
              'access_token': token
              } 
    
    response = requests.get(url, params = params) 
    data = response.json() 
    user_ids += data['response']['items'] 
    # Увеличиваем смещение на количество строк, которое мы уже выгрузили 
    offset += count 
print(len(user_ids)) 
print(user_ids[0])

for id in user_ids:
    pass

# Перечисляем параметры нашего запроса в словаре params
params = {'user_id': 1, 
          'v': 5.95, 
          'fields': 'sex,bdate', 
          'access_token': token, 
          'lang': 'ru'} 

response = requests.get(url, params=params) # Отправляем запрос
print(response.text) # Выводим текст ответа на экран

pprint(response.json()) # Выводим содержимое словаря, содержащего ответ, на экран

user = response.json()['response'][0]   # Извлекаем из словаря по ключу response информацию о первом пользователе
print(user['bdate'])                    # Выводим дату рождения первого пользователя на экран

# ОТПРАВКА СООБЩЕНИЙ
url = 'https://api.vk.com/method/messages.send' # Указываем адрес обращения