from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_ITEM = ".inventory_item"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    ITEM_PRICE = ".inventory_item_price"

    def add_item_to_cart_by_name(self, item_name: str):
        item = self.page.locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        item.get_by_role("button", name="Add to cart").click()
        return self

    def cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.text_of(self.CART_BADGE))
        return 0

    def open_cart(self):
        self.click(self.CART_LINK)
        return self

    def sort_by(self, option_value: str):
        self.select_option(self.SORT_DROPDOWN, option_value)
        return self

    def get_all_prices(self) -> list[float]:
        prices = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in prices]
