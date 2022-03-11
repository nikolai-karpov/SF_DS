import requests                 # Импортируем библиотеку requests
from bs4 import BeautifulSoup   # Импортируем библиотеку BeautifulSoup
from pprint import pprint       # Импортируем функцию pprint()
import time                     # Импортируем модуль time


token = 'c22b3e0bc22b3e0bc22b3e0b0ec250afc0cc22bc22b3e0ba001682b457a61bc5e48e073'

"""
-   https://api.vk.com/method — домен и URL запроса API; обычно не меняется;

-   users.get — название метода, который отдаёт определённый отчёт, 
    в нашем случае это метод для получения информации о пользователе;
    
-   user_id и v — параметры запроса: идентификатор пользователя, 
    о котором хотим получить информацию (в нашем примере мы запрашиваем информацию о первом пользователе), 
    и номер версии API;
    
-   token — токен, который выдаётся только пользователям, имеющим право просматривать определённые данные, 
    например показания счётчиков Яндекс.Метрики вашего проекта; 
    на все остальные запросы без корректного токена система отвечает отказом.

"""
"""
url = 'https://api.vk.com/method/users.get'         # Указываем адрес страницы к которой делаем запрос

# Перечисляем параметры нашего запроса в словаре params
params = {'user_id': 1, 
          'v': 5.95, 
          'fields': 'sex,bdate', 
          'access_token': token, 
          'lang': 'ru'} 

#response = requests.get(url, params=params) # Отправляем запрос
#print(response.text) # Выводим текст ответа на экран

#pprint(response.json()) # Выводим содержимое словаря, содержащего ответ, на экран

#user = response.json()['response'][0]   # Извлекаем из словаря по ключу response информацию о первом пользователе
#print(user['bdate'])                    # Выводим дату рождения первого пользователя на экран


# запрашивать информацию о множестве (до 1 000) пользователей одновременно
ids = ",".join(map(str, range(1, 4)))   # Формируем строку, содержащую информацию о поле id первых трёх пользователей

# Формируем строку параметров
params = {'user_ids': ids, 
          'v': 5.95, 
          'fields': 'bday', 
          'access_token': token, 
          'lang': 'ru'}                         

# Посылаем запрос, 
# полученный ответ в формате JSON-строки преобразуем в словарь 
# и выводим на экран его содержимое, используя функцию pprint()
#pprint(requests.get(url, params=params).json()) 


# Используя API, определите долю женщин (sex=1) среди пользователей с id от 1 до 500
ids = ",".join(map(str, range(1, 500)))   # Формируем строку, содержащую информацию о поле id первых трёх пользователей
params = {'user_id': ids, 
          'v': 5.95, 
          'fields': 'sex', 
          'access_token': token, 
          'lang': 'ru'}

response = requests.get(url, params=params) # Отправляем запрос

count_women = 0
count_men = 0
for i in range(0, 499):
    user = response.json()['response'][i]       # Извлекаем из словаря по ключу response информацию о текущем пользователе
    if user['sex'] == 1:
        count_women += 1
    if user['sex'] == 2:
        count_men += 1        

#print('Женщин: ', count_women)        
#print('Мужчин: ', count_men)   
#print('Доля женщин:', round(count_women/(count_women+count_men), 2))

# СБОР ИНФОРМАЦИИ ИЗ ГРУПП
url = 'https://api.vk.com/method/groups.getMembers' # Указываем адрес обращения

# Формируем строку параметров
params = {'group_id': 'dwgformat', 
          'v': 5.95, 
          'access_token': token
          } 
response = requests.get(url, params = params)   # Посылаем запрос
data = response.json()                          # Ответ сохраняем в переменной data в формате словаря

# count - общее число участников группы
#  items - id участников группы
#print(data)                                     # Выводим содержимое переменной data на экран (отображён фрагмент)

# Выводим на экран количество элементов словаря 
#print(len(data['response']['items'])) # получили мы только первую тысячу пользователей группы

# выведем на экран первые 20 пользователей из нашей первой попытки получить информацию о 1000 пользователей, 
# чтобы мы могли сверить результат выгрузки из 20 пользователей:
#users_for_checking = data['response']['items'][:20] # Загружаем в переменную информацию об id первых 20 пользователей в виде списка
#print(users_for_checking)                           # Выводим перечень id первых 20 пользователей

# используем count и offset, чтобы получить те же id по пять за раз:
count = 1000 
offset = 0 
user_ids = [] 
max_count = data['response']['count'] 
while offset < max_count: 
    # Будем выгружать по count=5 пользователей, 
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
#print(len(user_ids)) 


# ОГРАНИЧЕНИЕ ПО ЧАСТОТЕ ЗАПРОСОВ
count = 1000 
offset = 0  
user_ids = []  
while offset < 5000: 
    params = {'group_id': 'dwgformat', 
              'v': 5.95, 'count': count, 
              'offset': offset, 
              'access_token': token
              } 
    response = requests.get(url, params = params) 
    data = response.json() 
    user_ids += data['response']['items'] 
    offset += count 
    print('Ожидаю 0.5 секунды...') 
    time.sleep(0.5) 
#print('Цикл завершен, offset =',offset) 

"""
# ЛАЙКИ, РЕПОСТЫ И КОММЕНТАРИИ
# Для получения информации о сообщениях на стене в API ВКонтакте предусмотрен метод wall.get.
url = 'https://api.vk.com/method/wall.get' # Указываем адрес страницы, к которой делаем запрос

# count - общее количество сообщений в новостной ленте
# items - сами сообщения
params = {'domain': 'dwgformat', 
          'filter': 'owner', 
          'count': 1000, 
          'offset': 0, 
          'access_token': token, 
          'v': 5.95
          } 
response = requests.get(url, params = params) 
#pprint(response.json()) 

# Посмотрим на информацию об отдельном сообщении:
#pprint(response.json()['response']['items'][0])


# соберём итоговую статистику для последних десяти непустых сообщений в словарь stats
# В качестве ключа будем использовать начало сообщения
# в качестве значения — список с тремя интересующими нас метриками и временем публикации (комментарии, лайки, репосты, дата публикации)
stats = {} 
count_post = 0 # Счётчик «непустых» сообщений
for record in response.json()['response']['items'][:]:
    title = record['text'][:30] 
    if title: 
        stats[title] = [record['comments']['count'], 
                        record['likes']['count'], 
                        record['reposts']['count'], 
                        record['date']] 
        count_post += 1 
    if count_post < 10: 
        continue 
    else: 
        break 
pprint(stats)