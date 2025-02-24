import pytest

from main import Category, Product


@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 1000.0, 5)


@pytest.fixture
def sample_category(sample_product):
    return Category("Test Category", "Test Description", [sample_product])


@pytest.fixture(autouse=True)
def reset_counters():
    # Сбрасываем счетчики перед каждым тестом
    Category.category_count = 0
    Category.product_count = 0


def test_product_initialization(sample_product):
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.price == 1000.0
    assert sample_product.quantity == 5


def test_category_initialization(sample_category):
    assert sample_category.name == "Test Category"
    assert sample_category.description == "Test Description"
    assert len(sample_category.products) == 1
    assert isinstance(sample_category.products[0], Product)


def test_category_counters_single_category(sample_category):
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_category_counters_multiple_categories(sample_product):
    # Создаем первую категорию
    Category("Category 1", "Desc", [sample_product])
    assert Category.category_count == 1
    assert Category.product_count == 1

    # Создаем вторую категорию
    Category("Category 2", "Desc", [sample_product, sample_product])
    assert Category.category_count == 2
    assert Category.product_count == 3


def test_empty_category():
    category = Category("Empty", "Desc", [])
    assert category.category_count == 1
    assert category.product_count == 0


def test_products_list_content():
    p1 = Product("P1", "Desc", 100, 2)
    p2 = Product("P2", "Desc", 200, 3)
    category = Category("Test", "Desc", [p1, p2])

    assert len(category.products) == 2
    assert category.products[0].name == "P1"
    assert category.products[1].price == 200


def test_class_vs_instance_attributes():
    category = Category("Test", "Desc", [])
    assert category.category_count == 1  # Проверяем атрибут класса
    assert Category.category_count == 1  # Проверяем через класс


def test_edge_cases():
    # Тест с нулевой ценой
    p = Product("Free", "Free product", 0.0, 0)
    assert p.price == 0.0

    # Тест с очень большими значениями
    big_product = Product("Big", "Huge quantity", 999999.99, 1000000)
    assert big_product.quantity == 1000000
