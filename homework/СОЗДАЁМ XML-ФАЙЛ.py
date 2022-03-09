import xml.etree.ElementTree as ET

new_root = ET.Element('menu')

# добавлять новые узлы 
# В метод SubElement() мы передали первым аргументом узел, к которому добавляем потомка, 
# вторым аргументом — наименование нового тега (dish),  
# третьим аргументом — наименование атрибута нового узла( name ) и его значение.
dish1 = ET.SubElement(new_root, 'dish', name='Кура')
dish2 = ET.SubElement(new_root, 'dish', name='Греча')


# Добавим в создаваемую структуру по три потомка (атрибута) к двум новым узлам
price1 = ET.SubElement(dish1, "price").text = "40"
weight1 = ET.SubElement(dish1, "weight").text = "300"
class1 = ET.SubElement(dish1, "class").text = "Мясо"

price2 = ET.SubElement(dish2, "price").text = "20"
weight2 = ET.SubElement(dish2, "weight").text = "200"
class2 = ET.SubElement(dish2, "class").text = "Крупа"


# Проверим визуально корректность созданной нами структуры
for dish in new_root:
    for param in dish:
        print(dish.attrib['name'], param.tag, param.text)
    print()
    
    
# СОХРАНЕНИЕ XML-ФАЙЛА
# Преобразуем созданный нами объект типа ElementTree.Element в строку c помощью метода tostring()
new_root_string = ET.tostring(new_root)
with open("homework/data/new_menu.xml", "wb") as f:
    f.write(new_root_string)
    
# Для этого мы передаём в класс ElementTree() наше дерево (не его строковое представление) и вызываем метод write(). 
# В метод мы передаём путь к новому файлу и нужную нам кодировку.
ET.ElementTree(new_root).write('homework/data/new_menu_good.xml', encoding="utf-8")