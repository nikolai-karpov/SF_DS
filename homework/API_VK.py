import requests                 # Импортируем библиотеку requests
from bs4 import BeautifulSoup   # Импортируем библиотеку BeautifulSoup
from pprint import pprint       # Импортируем функцию pprint()


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

url = 'https://api.vk.com/method/users.get'         # Указываем адрес страницы к которой делаем запрос

# Перечисляем параметры нашего запроса в словаре params
params = {'user_id': 1, 
          'v': 5.95, 
          'fields': 'sex,bdate', 
          'access_token': token, 
          'lang': 'ru'} 

response = requests.get(url, params=params) # Отправляем запрос
#print(response.text) # Выводим текст ответа на экран

#pprint(response.json()) # Выводим содержимое словаря, содержащего ответ, на экран

user = response.json()['response'][0]   # Извлекаем из словаря по ключу response информацию о первом пользователе
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

print('Женщин: ', count_women)        
print('Мужчин: ', count_men)   
print('Доля женщин:', round(count_women/(count_women+count_men), 2))

# СБОР ИНФОРМАЦИИ ИЗ ГРУПП