from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class LoggingMixin:
    def __init__(self, *args, **kwargs):
        params = ", ".join([repr(a) for a in args] + [f"{k}={repr(v)}" for k, v in kwargs.items()])
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: ({params})")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    def __init__(self, *args, **kwargs):
        """Базовый конструктор для корректной работы миксина"""
        pass

    @property
    @abstractmethod
    def price(self) -> float:
        pass

    @price.setter
    @abstractmethod
    def price(self, value: float) -> None:
        pass

    @classmethod
    @abstractmethod
    def new_product(cls, product_data: Dict, products_list: Optional[List["BaseProduct"]] = None) -> "BaseProduct":
        pass


class Product(LoggingMixin, BaseProduct):
    def __init__(self, name: str, description: str, price: float, quantity: int):
        super().__init__(name=name, description=description, price=price, quantity=quantity)
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, new_price: float) -> None:
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

    def __add__(self, other) -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных классов")
        return self.price * self.quantity + other.price * other.quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    @classmethod
    def new_product(cls, product_data: Dict, products_list: Optional[List["Product"]] = None) -> "Product":
        if products_list:
            for product in products_list:
                if product.name == product_data["name"]:
                    product.quantity += product_data["quantity"]
                    product.price = max(product.price, product_data["price"])
                    return product
        return cls(**product_data)


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
        params = (
            f"name={repr(name)}, description={repr(description)}, price={repr(price)}, quantity={repr(quantity)}"
            f"efficiency={repr(efficiency)}, model={repr(model)}, memory={repr(memory)}, color={repr(color)}"
        )
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: ({params})")

    @classmethod
    def new_product(cls, product_data: Dict, products_list: Optional[List["Smartphone"]] = None) -> "Smartphone":
        return cls(**product_data)


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
        params = (
            f"name={repr(name)}, description={repr(description)}, price={repr(price)}, quantity={repr(quantity)}"
            f"country={repr(country)}, germination_period={repr(germination_period)}, color={repr(color)}"
        )
        print(f"Создан объект класса {self.__class__.__name__} с параметрами: ({params})")

    @classmethod
    def new_product(cls, product_data: Dict, products_list: Optional[List["LawnGrass"]] = None) -> "LawnGrass":
        return cls(**product_data)


class Category:
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников.")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(p) for p in self.__products)

    def __len__(self) -> int:
        return len(self.__products)

    def __str__(self) -> str:
        total = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов: {total} шт."
