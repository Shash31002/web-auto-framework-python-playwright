import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.config_reader import load_json, load_yaml

users = load_json("users.json")
checkout_data = load_yaml("checkout_data.yaml")


@pytest.fixture
def logged_in_inventory_page(page):
    user = users["valid_user"]
    LoginPage(page).open().login(user["username"], user["password"])
    return InventoryPage(page)


@pytest.mark.smoke
def test_add_item_updates_cart_badge(logged_in_inventory_page):
    inventory = logged_in_inventory_page
    inventory.add_item_to_cart_by_name(checkout_data["products"][0])

    assert inventory.cart_count() == 1


@pytest.mark.regression
def test_add_multiple_items_updates_cart_count(logged_in_inventory_page):
    inventory = logged_in_inventory_page
    for product in checkout_data["products"]:
        inventory.add_item_to_cart_by_name(product)

    assert inventory.cart_count() == len(checkout_data["products"])


@pytest.mark.regression
def test_sort_low_to_high_orders_prices_ascending(logged_in_inventory_page):
    inventory = logged_in_inventory_page
    inventory.sort_by("lohi")

    prices = inventory.get_all_prices()
    assert prices == sorted(prices)
