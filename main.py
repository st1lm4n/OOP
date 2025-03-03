class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self):
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float):
        """Сеттер для цены с проверкой и подтверждением."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная.")
            return

        # Если цена понижается, запрашиваем подтверждение
        if new_price < self.__price:
            confirmation = input(f"Цена понижается с {self.__price} до {new_price}. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено.")
                return

        # Устанавливаем новую цену
        self.__price = new_price
        print(f"Цена успешно изменена на {new_price}.")

    @classmethod
    def new_product(cls, product_data: dict, products_list: list = None):
        """
        Класс-метод для создания нового товара.
        :param product_data: Словарь с данными о товаре (name, description, price, quantity).
        :param products_list: Список существующих товаров (опционально).
        :return: Объект Product.
        """
        name = product_data.get("name")
        description = product_data.get("description")
        price = product_data.get("price")
        quantity = product_data.get("quantity")

        if products_list is not None:
            # Поиск товара с таким же именем
            for product in products_list:
                if product.name == name:
                    # Обновляем количество и цену
                    product.quantity += quantity
                    product.price = max(product.price, price)
                    return product

            # Если товар не найден, создаем новый и добавляем в список
            new_product = cls(name, description, price, quantity)
            products_list.append(new_product)
            return new_product

        # Если список не передан, просто создаем новый товар
        return cls(name, description, price, quantity)


class Category:
    category_count = 0  # Общее количество категорий
    product_count = 0  # Общее количество товаров во всех категориях

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products  # Приватный атрибут для списка товаров
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product):
        """Добавляет товар в приватный список товаров."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product.")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Геттер для получения списка товаров в виде строки."""
        products_info = []
        for product in self.__products:
            products_info.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.")
        return "\n".join(products_info)

    def __len__(self):
        """Возвращает количество товаров в категории."""
        return len(self.__products)

    def __str__(self):
        """Возвращает строковое представление категории."""
        return f"{self.name}, количество товаров: {len(self)}"


if __name__ == "__main__":
    # Создаем товары
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаем категорию
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    # Выводим список товаров
    print(category1.products)

    # Добавляем новый товар в категорию
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)

    # Выводим общее количество товаров
    print(f"Общее количество товаров: {category1.product_count}")

    # Создаем новый товар через класс-метод
    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    # Пытаемся изменить цену
    new_product.price = 800  # Запросит подтверждение
    print(new_product.price)

    # Пытаемся установить отрицательную цену
    new_product.price = -100  # Выведет сообщение об ошибке
    print(new_product.price)

    # Пытаемся установить нулевую цену
    new_product.price = 0  # Выведет сообщение об ошибке
    print(new_product.price)
