# Проект 1. Анализ вакансий на hh.ru

## Оглавление
* [1. Описание проекта](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Описание-проекта)
* [2. Какой кейс решаем?](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Какой-кейс-решаем)
* [3. Краткая информация о данных](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Краткая-информация-о-данных)
* [4. Этапы работы над проектом](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Этапы-работы-над-проектом)
* [5. Результат](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Результат)
* [6. Выводы](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Выводы)

### Описание проекта
Угадать загаданное компьютером число за минимальное кол-во попыток.

:arrow_up:[к оглавлению](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Оглавление)


### Какой кейс решаем?
Компания HeadHunter хочет построить модель, которая бы автоматически определяла примерный уровень заработной платы, подходящей пользователю, исходя из информации, которую он указал о себе

**Наша задача преобразовать, исследовать и очистить**
- Компьютер загадывает число от 0 до 100, и нам его нужно угадать. Под "угадать" подразумевается "написать программу, которая угадывает число".
- Аогоритм учитывает информацию о том, больше ли случайное число или меньше нужного нам.

**Наш проект будет состоять из четырёх частей:**
1. Базовый анализ структуры данных
2. Преобразование данных
3. Разведывательный анализ
4. Очистка данных

**ДЛЯ УСПЕШНОГО ВЫПОЛНЕНИЯ ПРОЕКТА НЕОБХОДМО**
- Определить все признаки, в которых есть пропуски в данных
- Преобразовать признаки в удобный для анализа формат
- Выделить сгрупированные данные в отдельные признаки
- Провести ислледование данных
- Сделать выводы

### Краткая информация о данных
Пол, Возраст, Дата рождения, Последняя/нынешняя должность, Опыт работы, Последнее/нынешнее место работы, Желаемая зарплата, Город, Уровень образования, Год выпуска, ВУЗ, Специальность

:arrow_up:[к оглавлению](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Оглавление)

### Этапы работы над проектом
- Исследование структуры данных
- Преобразование данных
- Исследование зависимостей в данных
- Очистка данных

:arrow_up:[к оглавлению](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Оглавление)

### Результат
- Преобразован признак «Образование и ВУЗ» из формата <Уровень образования год выпуска ВУЗ специальность...> приведен к четырем категориям: «высшее», «неоконченное высшее», «среднее специальное» и «среднее».
- Из признака «Пол, возраст» выделены два новых признака «Пол» и «Возраст».
- Преобразован признак «Опыт работы» приведен к единому формату месяцы.
- Из признака «Город, переезд, командировки» выделены отдельные признаки «Город», «Готовность к переезду», «Готовность к командировкам»
- В признаке «Город» создано четыре категории: «Москва», «Санкт-Петербург», «город-миллионник» и «другие». 
- Из признаков «Занятость» и «График» созданы признаки-«мигалки» (True и False): полная занятость,частичная занятость, проектная работа, стажировка, волонтёрство.
- Преобразован признак заработной платы «ЗП» в рубли по курсу на день публикации анкеты

:arrow_up:[к оглавлению](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Оглавление)

### Выводы
- Высшее образование по медианному показателю оплачивается выше всех остальных категорий.
- Наименьшие уровни желаемой заработной платы наблюдаются в категории среднее и среднеспециальное.
- Медианные уровни желаемой заработной платы вышел в Москве и Санкт-Петербурге, и их размах в этих городах соответственно шире.
- Считаю, что признак города при прогнозировании заработной платы важен.
- Медианная заработная плата соискателей, готовых и к переезду, и к командировкам равна 66 тыс.руб.
- Наибольший уровень ожидаемой зарплаты демонстрирует категория "Готов к переезду и командировкам".
- Наименьший уровень зарплаты наблюдается у категории "Не готов к переезду и командировкам".
- Готовность соискателей к командировкам демонстрирует очевидные более высокие ожидания по зарплате.
- Для категории образования "высшее"наблюдается самый быстрый карьерный рост (то есть интенсивность роста заработной платы наибольшая).
- Чем ниже уровень образования, тем меньше динамика роста уровня заработной платы.
- 7 точек находятся на линии "опыт работы равен возрасту человека" либо выше её - это очевидные аномалии в данных.
- В Москве соискатели с высшим образованием запрашивают более высокий уровень зарплаты по отношению к другим регионам.
- В Москве и Санкт-Петербурге наблюдается закономерность, где соискатели со средним образованием ожидают тот же уровень зарплат, что и со среднеспециальным.
- В городах миллиониках показатели тождествены другим регионам страны.
- Наблюдается существенное различие в размере ожидаемой зарплаты между группой Москва-Питер и другие города включая миллионники.
- Средний возраст готовых к переезду и командировкам 30-33 года, что в свою очердь совпадает со средним возрастом соискателей с высшим и средним образованием.
- Среди соискателей готовых к переезду и командировкам значительно больше тех кто с высшим образованием.

:arrow_up:[к оглавлению](https://github.com/nikolai-karpov/SF_DS/blob/main/project1/README.md#Оглавление)
