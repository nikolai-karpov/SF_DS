import schedule # Импортируем модуль schedule
import time 


# ПОСТАНОВКА ЗАДАЧИ
def task(): 
    print('Hello! I am a task!') 
    return 


# Для запуска задачи через определённые интервалы времени в модуле schedule используется метод every()
schedule.every(15).minutes.do(task)

# Если бы мы хотели запускать задачу, например, каждый час, то могли бы написать:
# schedule.every(1).hour.do(task) 


# ВЫПОЛНЕНИЕ ФУНКЦИИ

while True: 
    schedule.run_pending()  # будет проверять, нет ли задачи, которую пора выполнить.
    time.sleep(1)           # Для создания паузы мы будем использовать метод sleep
