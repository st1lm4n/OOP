from abc import ABC, abstractmethod
from typing import List, Optional


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @property
    @abstractmethod
    def price(self):
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["BaseProduct"]] = None) -> "BaseProduct":
        pass


class LoggingMixin:
    def __init__(self, *args, **kwargs):
        params = [repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()]
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: {', '.join(params)}")
        super().__init__(*args, **kwargs)


class Product(BaseProduct, LoggingMixin):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price: float):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная.")
            return

        if new_price < self._price:
            confirmation = input(f"Цена понижается с {self._price} до {new_price}. Подтвердите действие (y/n): ")
            if confirmation.lower() != "y":
                print("Изменение цены отменено.")
                return

        self._price = new_price
        print(f"Цена успешно изменена на {new_price}.")

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["Product"]] = None) -> "Product":
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


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["Smartphone"]] = None) -> "Smartphone":
        return super().new_product(product_data, products_list)


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    @classmethod
    def new_product(cls, product_data: dict, products_list: Optional[List["LawnGrass"]] = None) -> "LawnGrass":
        return super().new_product(product_data, products_list)


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
            raise TypeError("Можно добавлять только объекты класса Product или его наследников.")
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
