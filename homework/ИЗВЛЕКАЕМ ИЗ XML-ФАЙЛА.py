import xml.etree.ElementTree as ET # Импортируем модуль ElementTree

tree = ET.parse('homework/data/menu.xml')

# КОРЕНЬ
# Запишем в переменную root корневой узел дерева tree 
root = tree.getroot()

# и посмотрим, как выглядит содержимое переменной root
print(root)

# Какой тип у этого объекта?
print(type(root))


# ПОТОМКИ
# посмотреть список потомков корневого узла
print(list(root))

# получить список потомков второго блюда в нашем меню и вывести его на экран
print(list(root[1]))


# АТРИБУТЫ И ТЕГИ
# Выведем на экран атрибуты первого блюда
print(root[0].attrib)

# возьмём узел price первого блюда из меню
print(root[0][0])

# Теперь прочитаем значение этого узла с помощью text
print(root[0][0].text)

# наименование тега корневого узла
print(root.tag)

# Какое наименование имеет тег узла root[0][2]?
print(root[0][2].tag)


# ИСПОЛЬЗОВАНИЕ ЦИКЛОВ
for dish in root:
    for param in dish:
        print(dish.attrib['name'], param.tag, param.text)
    print()