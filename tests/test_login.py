import pytest
from pages.login_page import LoginPage
from utils.config_reader import load_json

users = load_json("users.json")


@pytest.mark.smoke
def test_valid_login_lands_on_inventory(page):
    login_page = LoginPage(page).open()
    user = users["valid_user"]
    login_page.login(user["username"], user["password"])

    login_page.wait_for_url_contains("inventory.html")
    assert "inventory.html" in page.url


@pytest.mark.regression
def test_locked_out_user_sees_error(page):
    login_page = LoginPage(page).open()
    user = users["locked_user"]
    login_page.login(user["username"], user["password"])

    assert "locked out" in login_page.get_error_message().lower()


@pytest.mark.regression
@pytest.mark.parametrize("username,password", [
    ("", ""),
    ("standard_user", ""),
    ("", "secret_sauce"),
])
def test_login_requires_credentials(page, username, password):
    login_page = LoginPage(page).open()
    login_page.login(username, password)

    assert login_page.is_visible(login_page.ERROR_MESSAGE)
