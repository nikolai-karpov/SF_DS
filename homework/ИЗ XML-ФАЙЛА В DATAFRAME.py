import xml.etree.ElementTree as ET

# Загрузить XML-структуру файла menu.xml в переменную root 
tree = ET.parse('homework/data/menu.xml')    
root = tree.getroot()

import pandas as pd

# Создать пустой DataFrame (в него будем постепенно загружать информацию из XML-файла)
# В создаваемом DataFrame четыре столбца — название блюда (name), его цена (price), вес (weight) и класс (class)
column_names = ['name', 'price', 'weight', 'class']
df = pd.DataFrame(columns=column_names)

for dish in root:
    row = [dish.attrib['name'], dish[0].text, dish[1].text, dish[2].text]
    df = df.append(pd.Series(row, index=column_names), ignore_index=True)

print(df)