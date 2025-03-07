import json

from main import Category, Product


def load_from_json(filename: str) -> list[Category]:
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    categories = []
    for category_data in data["categories"]:
        products = [
            Product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                quantity=product["quantity"],
            )
            for product in category_data["products"]
        ]
        category = Category(name=category_data["name"], description=category_data["description"], products=products)
        categories.append(category)
    return categories
