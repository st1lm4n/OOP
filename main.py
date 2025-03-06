class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная.")
            return

        if new_price < self.__price:
            confirmation = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено.")
                return

        self.__price = new_price
        print(f"Цена успешно изменена на {new_price}.")

    def __add__(self, other):
        if isinstance(other, Product):
            return self.price * self.quantity + other.price * other.quantity
        raise TypeError("Можно складывать только объекты класса Product")

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        if products_list:
            for product in products_list:
                if product.name == name:
                    product.quantity += quantity
                    product.price = max(product.price, price)
                    return product
            new_product = cls(name, description, price, quantity)
            products_list.append(new_product)
            return new_product
        return cls(name, description, price, quantity)


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product.")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        return "\n".join(str(product) for product in self.__products)

    def __len__(self):
        return len(self.__products)

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        return CategoryIterator(self)


class CategoryIterator:
    def __init__(self, category):
        self.products = category._Category__products
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.products):
            product = self.products[self.index]
            self.index += 1
            return product
        raise StopIteration


# if __name__ == "__main__":
#     # Создаем товары
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     # Создаем категорию
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3],
#     )
#
#     # Выводим список товаров
#     print(category1.products)
#
#     # Добавляем новый товар в категорию
#     product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
#     category1.add_product(product4)
#     print(category1.products)
#
#     # Выводим общее количество товаров
#     print(f"Общее количество товаров: {category1.product_count}")
#
#     # Создаем новый товар через класс-метод
#     new_product = Product.new_product(
#         {
#             "name": "Samsung Galaxy S23 Ultra",
#             "description": "256GB, Серый цвет, 200MP камера",
#             "price": 180000.0,
#             "quantity": 5,
#         }
#     )
#     print(new_product.name)
#     print(new_product.description)
#     print(new_product.price)
#     print(new_product.quantity)
#
#     # Пытаемся изменить цену
#     new_product.price = 800  # Запросит подтверждение
#     print(new_product.price)
#
#     # Пытаемся установить отрицательную цену
#     new_product.price = -100  # Выведет сообщение об ошибке
#     print(new_product.price)
#
#     # Пытаемся установить нулевую цену
#     new_product.price = 0  # Выведет сообщение об ошибке
#     print(new_product.price)
#
# if __name__ == '__main__':
#     product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
#     product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
#     product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
#
#     print(str(product1))
#     print(str(product2))
#     print(str(product3))
#
#     category1 = Category(
#         "Смартфоны",
#         "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
#         [product1, product2, product3]
#     )
#
#     print(str(category1))
#
#     print(category1.products)
#
#     print(product1 + product2)
#     print(product1 + product3)
#     print(product2 + product3)
