from pages.base_page import BasePage


class CartPage(BasePage):
    CHECKOUT_BUTTON = "#checkout"

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        return self


class CheckoutStepOnePage(BasePage):
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    ZIP_CODE = "#postal-code"
    CONTINUE_BUTTON = "#continue"

    def fill_info(self, first_name: str, last_name: str, zip_code: str):
        self.fill(self.FIRST_NAME, first_name)
        self.fill(self.LAST_NAME, last_name)
        self.fill(self.ZIP_CODE, zip_code)
        self.click(self.CONTINUE_BUTTON)
        return self


class CheckoutStepTwoPage(BasePage):
    FINISH_BUTTON = "#finish"
    TOTAL_LABEL = ".summary_total_label"

    def finish_order(self):
        self.click(self.FINISH_BUTTON)
        return self

    def get_total(self) -> str:
        return self.text_of(self.TOTAL_LABEL)


class CheckoutCompletePage(BasePage):
    COMPLETE_HEADER = ".complete-header"

    def get_confirmation_message(self) -> str:
        return self.text_of(self.COMPLETE_HEADER)
