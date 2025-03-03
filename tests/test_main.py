import pytest

from main import Category, Product


def test_products_getter():
    # Создаем товары с указанием всех необходимых аргументов
    product1 = Product("Product 1", "Description 1", 100.0, 5)
    product2 = Product("Product 2", "Description 2", 200.0, 10)

    # Создаем категорию с этими товарами
    category = Category("Test Category", "Test Description", [product1, product2])

    # Проверяем вывод геттера
    expected_output = "Product 1, 100.0 руб. Остаток: 5 шт.\n" "Product 2, 200.0 руб. Остаток: 10 шт."
    assert category.products == expected_output

    # Проверяем, что нельзя изменить список товаров через геттер
    with pytest.raises(AttributeError):
        category.products = []


def test_price_setter():
    product = Product("Test Product", "Test Description", 100.0, 5)

    # Пытаемся установить нулевую цену
    product.price = 0
    assert product.price == 100.0  # Цена не изменилась

    # Пытаемся установить отрицательную цену
    product.price = -50
    assert product.price == 100.0  # Цена не изменилась

    # Пытаемся понизить цену (с подтверждением)
    # Симулируем ввод пользователя "y"
    import builtins

    original_input = builtins.input
    builtins.input = lambda _: "y"
    product.price = 80.0
    assert product.price == 80.0  # Цена изменена
    builtins.input = original_input  # Восстанавливаем оригинальный input

    # Пытаемся понизить цену (без подтверждения)
    builtins.input = lambda _: "n"
    product.price = 70.0
    assert product.price == 80.0  # Цена не изменилась
    builtins.input = original_input

    # Пытаемся повысить цену
    product.price = 120.0
    assert product.price == 120.0  # Цена изменена


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 100.0, 5)


def test_price_getter(sample_product):
    """Проверяем, что геттер возвращает корректную цену"""
    assert sample_product.price == 100.0


def test_negative_price_setter(sample_product, capsys):
    """Проверяем блокировку отрицательной цены"""
    sample_product.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 100.0


def test_zero_price_setter(sample_product, capsys):
    """Проверяем блокировку нулевой цены"""
    sample_product.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert sample_product.price == 100.0


def test_price_decrease_with_confirmation(sample_product, monkeypatch):
    """Проверяем успешное понижение цены с подтверждением"""
    # Симулируем ввод 'y'
    monkeypatch.setattr("builtins.input", lambda _: "y")
    sample_product.price = 80.0
    assert sample_product.price == 80.0


def test_price_decrease_without_confirmation(sample_product, monkeypatch, capsys):
    """Проверяем отмену понижения цены"""
    # Симулируем ввод 'n'
    monkeypatch.setattr("builtins.input", lambda _: "n")
    sample_product.price = 80.0
    captured = capsys.readouterr()
    assert "Изменение цены отменено" in captured.out
    assert sample_product.price == 100.0


def test_price_increase(sample_product):
    """Проверяем повышение цены без подтверждения"""
    sample_product.price = 120.0
    assert sample_product.price == 120.0


def test_old_functionality(sample_product):
    """Проверяем работу старой функциональности"""
    # Проверка атрибутов
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.quantity == 5

    # Проверка изменения количества
    sample_product.quantity = 10
    assert sample_product.quantity == 10
