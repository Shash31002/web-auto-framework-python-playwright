import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import (
    CartPage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
    CheckoutCompletePage,
)
from utils.config_reader import load_json, load_yaml

users = load_json("users.json")
checkout_data = load_yaml("checkout_data.yaml")


@pytest.mark.smoke
def test_end_to_end_checkout_flow(page):
    user = users["valid_user"]
    buyer = checkout_data["valid_checkout"]

    LoginPage(page).open().login(user["username"], user["password"])

    inventory = InventoryPage(page)
    inventory.add_item_to_cart_by_name(checkout_data["products"][0])
    inventory.open_cart()

    CartPage(page).proceed_to_checkout()

    CheckoutStepOnePage(page).fill_info(
        buyer["first_name"], buyer["last_name"], buyer["zip_code"]
    )

    step_two = CheckoutStepTwoPage(page)
    assert "Total" in step_two.get_total()
    step_two.finish_order()

    confirmation = CheckoutCompletePage(page).get_confirmation_message()
    assert "Thank you" in confirmation
