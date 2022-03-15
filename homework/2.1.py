from pprint import pprint       # Импортируем функцию pprint()

def apply_discounts(products, stocks):
    """
    Напишите функцию apply_discounts(), которая снижает цену продуктов в словаре products на указанный в словаре stocks процент. 
    Функция должна вернуть результирующий словарь, ключи которого — товары, а значения — новые цены.
    Если продукта из словаря stocks нет в словаре products, то его необходимо пропустить. Цены округлите до второго знака после запятой.
    """
    keys = stocks.keys()
    for key in keys:
        discount = stocks[key].replace('%', '')
        discount = int(discount)/100
        products[key] = round((products[key] * discount), 2)
    return products


if __name__ == '__main__':
    products={
        "Oranges (packaged)": 114.99, 
        "Candy (Rotfront)": 280.00,
        "Boiled sausage": 199.99,
        "Juice J7 (orange)": 119.99,
        "Trout (Seven Seas)": 399.99
        }
    stocks = {
        "Boiled sausage": "33%",
        "Juice J7 (orange)": "12%",
        "Trout (Seven Seas)": "18%"
    }
    new_products = apply_discounts(products, stocks)
    pprint(new_products)