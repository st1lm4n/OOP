from io import StringIO
from unittest.mock import patch

import pytest

from main import Category, LawnGrass, Product, Smartphone, ZeroQuantityError


@pytest.fixture
def sample_product():
    return Product(name="Test", description="Desc", price=100.0, quantity=5)


@pytest.fixture
def sample_smartphone():
    return Smartphone(
        name="PhoneX",
        description="Flagship",
        price=1000.0,
        quantity=3,
        efficiency=95.5,
        model="X1",
        memory=256,
        color="Black",
    )


@pytest.fixture
def sample_lawn_grass():
    return LawnGrass(
        name="PremiumGrass",
        description="Green",
        price=50.0,
        quantity=10,
        country="USA",
        germination_period="2 weeks",
        color="Emerald",
    )


def test_product_creation_logging(capsys):
    """Проверка вывода лога при создании продукта"""
    Product(name="Test", description="Desc", price=100.0, quantity=5)
    captured = capsys.readouterr()
    assert "Создан объект класса Product" in captured.out
    assert "name='Test'" in captured.out
    assert "price=100.0" in captured.out


def test_smartphone_creation_logging(capsys):
    """Проверка вывода лога при создании смартфона"""
    Smartphone(
        name="PhoneX",
        description="Flagship",
        price=1000.0,
        quantity=3,
        efficiency=95.5,
        model="X1",
        memory=256,
        color="Black",
    )
    captured = capsys.readouterr()
    assert "Создан объект класса Smartphone" in captured.out
    assert "memory=256" in captured.out


def test_lawn_grass_creation_logging(capsys):
    """Проверка вывода лога при создании газона"""
    LawnGrass(
        name="PremiumGrass",
        description="Green",
        price=50.0,
        quantity=10,
        country="USA",
        germination_period="2 weeks",
        color="Emerald",
    )
    captured = capsys.readouterr()
    assert "Создан объект класса LawnGrass" in captured.out
    assert "germination_period='2 weeks'" in captured.out


def test_price_update_flow(sample_product):
    """Проверка корректного обновления цены"""
    sample_product.price = 150.0
    assert sample_product.price == 150.0


@patch("builtins.input", return_value="n")
def test_price_decline_cancellation(input_mock, sample_product):
    """Проверка отмены снижения цены"""
    sample_product.price = 80.0
    assert sample_product.price == 100.0  # Цена должна остаться прежней


def test_valid_product_addition(sample_product):
    """Проверка сложения товаров одного класса"""
    p2 = Product(name="Test2", description="Desc", price=200.0, quantity=3)
    total = sample_product + p2
    assert total == 100 * 5 + 200 * 3


def test_invalid_product_addition(sample_product, sample_smartphone):
    """Проверка ошибки при сложении разных классов"""
    with pytest.raises(TypeError) as excinfo:
        _ = sample_product + sample_smartphone
    assert "Нельзя складывать товары разных классов" in str(excinfo.value)


def test_new_product_creation():
    """Проверка фабричного метода для Product"""
    data = {"name": "NewProduct", "description": "NewDesc", "price": 300.0, "quantity": 10}
    p = Product.new_product(data)
    assert p.quantity == 10
    assert p.price == 300.0


def test_smartphone_new_product_creation():
    """Проверка фабричного метода для Smartphone"""
    data = {
        "name": "NewPhone",
        "description": "NewPhoneDesc",
        "price": 500.0,
        "quantity": 5,
        "efficiency": 98.0,
        "model": "X2",
        "memory": 512,
        "color": "White",
    }
    s = Smartphone.new_product(data)
    assert s.memory == 512
    assert s.model == "X2"


def test_category_operations(sample_product):
    """Проверка работы с категориями"""
    category = Category(name="Electronics", description="Tech", products=[])
    category.add_product(sample_product)

    assert len(category) == 1
    assert "Test" in category.products
    assert category.product_count == 1


def test_invalid_product_addition_to_category():
    """Проверка добавления неверного типа в категорию"""
    category = Category(name="Test", description="Desc", products=[])
    with pytest.raises(TypeError) as excinfo:
        category.add_product("invalid_product")
    assert "Можно добавлять только объекты класса Product" in str(excinfo.value)


def test_category_counters():
    """Проверка счетчиков категорий"""
    initial_count = Category.category_count
    Category(name="NewCat", description="Desc", products=[])
    assert Category.category_count == initial_count + 1


@patch("sys.stdout", new_callable=StringIO)
def test_full_product_lifecycle(mock_stdout):
    """Комплексный тест жизненного цикла продукта"""
    p = Product(name="Lifecycle", description="Test", price=200.0, quantity=10)

    p.price = 250.0

    category = Category(name="Test", description="Desc", products=[])
    category.add_product(p)

    assert "Создан объект класса Product" in mock_stdout.getvalue()
    assert "Цена успешно изменена на 250.0" in mock_stdout.getvalue()
    assert len(category) == 1


def test_product_creation_with_zero_quantity():
    with pytest.raises(ZeroQuantityError) as exc_info:
        Product("Test Product", "Test Description", 100.0, 0)
    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_category_middle_price_with_products():
    product1 = Product("Product1", "Desc1", 100.0, 5)
    product2 = Product("Product2", "Desc2", 200.0, 3)
    category = Category("Test Category", "Test Description", [product1, product2])

    assert category.middle_price() == 150.0


def test_category_middle_price_empty():
    category = Category("Empty Category", "Test Description", [])
    assert category.middle_price() == 0.0


def test_add_product_with_zero_quantity():
    with pytest.raises(ZeroQuantityError) as exc_info:  # Изменяем ожидаемое исключение
        Product("Invalid", "Desc", 50.0, 0)
    assert "Товар с нулевым количеством не может быть добавлен" in str(exc_info.value)


def test_category_initialization_with_invalid_products(capsys):

    valid_product = Product("Valid", "Desc", 100.0, 5)

    try:
        invalid_product = Product("Invalid", "Desc", 50.0, 0)
    except ZeroQuantityError:
        pass

    category = Category("Test", "Desc", [valid_product])
    captured = capsys.readouterr()

    assert "Ошибка при добавлении продукта" not in captured.out
    assert len(category) == 1


def test_product_addition():
    product1 = Product("Product1", "Desc1", 100.0, 5)
    product2 = Product("Product2", "Desc2", 200.0, 3)

    assert product1 + product2 == (100 * 5 + 200 * 3)


def test_price_change_confirmation(monkeypatch):
    product = Product("Test", "Desc", 100.0, 5)

    monkeypatch.setattr("builtins.input", lambda _: "y")
    product.price = 50.0
    assert product.price == 50.0

    monkeypatch.setattr("builtins.input", lambda _: "n")
    product.price = 30.0
    assert product.price == 50.0  # Цена должна остаться прежней


def test_category_counter():
    initial_categories = Category.category_count
    initial_products = Category.product_count

    product = Product("Test", "Desc", 100.0, 5)
    category = Category("Test", "Desc", [product])

    assert Category.category_count == initial_categories + 1
    assert Category.product_count == initial_products + 1


def test_smartphone_creation():
    smartphone = Smartphone("iPhone 15", "Flagship", 1000.0, 10, 95.0, "15 Pro", 256, "Space Gray")
    assert isinstance(smartphone, Product)
    assert smartphone.memory == 256
