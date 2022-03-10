import requests # Импортируем библиотеку requests
from bs4 import BeautifulSoup # Импортируем библиотеку BeautifulSoup

#url = 'https://www.cbr-xml-daily.ru/daily_json.js'  # Определяем значение URL страницы для запроса
#response = requests.get(url)                        # Делаем GET-запрос к ресурсу и результат ответа сохраняем в переменной response
#print(response.status_code)

url = 'https://nplus1.ru/news/2021/10/11/econobel2021' # Определяем адрес страницы
response = requests.get(url) # Выполняем GET-запрос, содержимое ответа присваивается переменной response
page = BeautifulSoup(response.text, 'html.parser') # Создаём объект BeautifulSoup, указывая html-парсер
#print(page.title) # Получаем тег title, отображающийся на вкладке браузера
#print(page.title.text) # Выводим текст из полученного тега, который содержится в атрибуте text


# ИЗВЛЕКАЕМ ЗАГОЛОВОК И ВРЕМЯ НАПИСАНИЯ СТАТЬИ
# Предположим, что мы знаем, что в HTML-коде рассматриваемой нами страницы заголовок статьи заключён в тег <h1>
#print(page.find('h1').text) # Применяем метод find() к объекту и выводим результат на экран

# получим информации о теге, который содержит дату/время написания статьи
#print(page.find('time').text) # Выводим на экран содержимое атрибута text тега time


# функцию wiki_header, которая по адресу страницы возвращает заголовок для статей на Wikipedia.
def wiki_header(url):
    """Функция возвращает заголовок для переданой странице

    Args:
        url (str): Адрес страницы
    
    Returns:
        [str]: [Заголовок]
    """
    page=BeautifulSoup(requests.get(url).text,'html.parser')
    header=page.find('h1').text
    return header


#print(wiki_header('https://en.wikipedia.org/wiki/Operating_system'))


#print(page.find('div', class_='body').text) # Выводим содержимое атрибута text тега div класса body js-mediator-article


# СБОР НЕСКОЛЬКИХ ЭЛЕМЕНТОВ: СОБИРАЕМ ВСЕ ССЫЛКИ НА СТРАНИЦЕ
# Попробуем использовать find():
url = 'https://en.wikipedia.org/wiki/List_of_programming_languages' # Задаём адрес ресурса
response = requests.get(url)                        # Делаем GET-запрос к ресурсу
page = BeautifulSoup(response.text, 'html.parser')  # Создаём объект BeautifulSoup
#print(page.find('a'))                               # Ищем ссылку по тегу <a> и выводим её на экран

# Если требуется получить больше элементов, необходимо воспользоваться методом find_all()
links = page.find_all('a')  # Ищем все ссылки на странице и сохраняем в переменной links в виде списка
#print(len(links))           # Выводим количество найденных ссылок

#print([link.text for link in links[500:510]]) # Выводим ссылки с 500 по 509 включительно

print([link.text for link in links[0:10]]) # Выводим ссылки с 1 по 9 включительно