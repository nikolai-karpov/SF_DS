"""Игра угадай число
Компьютер сам загадывает и сам угадывает число"""

import numpy as np
from numpy import random


def random_predict_2(number: int = 1) -> int:
    """Угадываем на random, используя информацию предыдущей попытки.
       Функция принимает загаданное число, корректирует границы в которых угадывает в соответствии с предыдущим результатом угалывания больше-меньше 
       и возвращает число попыток
    Args:
        number (int. optional): Загаданное число. Defaults to 1.
    Returns:
        int: Число попыток
    """

    count = 0                                           # Счетчик цикла
    min_predict = 1                                     # Границы угадывания min
    max_predict = 101                                   # Границы угадывания max
    
    while True:
        count += 1
        predict_number = np.random.randint(min_predict, max_predict)      # Предпалагаемое число
        if predict_number == number:
            break                                       # Выход из цикла, если угадали
        
        if predict_number > number:                     # Если предложенное число меньше угадываемого, корректируем максимальные границы угадывания
            max_predict = predict_number
        
        elif predict_number < number:                   # Если предложенное число больше угадываемого, корректируем минимальные границы угадывания
            min_predict = predict_number
    
    return (count)


def score_game(random_predict_2) -> int:
    """[За какое кол-во попыток в среднем угадываем]за 1000 подходов

    Args:
        random_predict ([type]): [Функция угадывания]

    Returns:
        int: [Среднее кол-во попыток]
    """
    
    count_ls = []                                           # Список в который сохраняем кол-во попыток
    np.random.seed(1)                                       # Фиксируем сид для воспроизводимости
    random_array = np.random.randint(1, 101, size=(1000))   # Высчитаваем средний показатель за 1000 запусков

    for number in random_array:
        count_ls.append(random_predict_2(number))
        
    score = int(np.mean(count_ls))                          # Вычисляем среднее значение в счетчике
    print(f'Ваш алгоритм в среднем угадывает за {score} попыток')
    return(score)


#if __name__ == '__main__':
# RUN

score_game(random_predict_2)