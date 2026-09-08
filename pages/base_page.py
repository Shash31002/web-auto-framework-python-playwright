"""
BasePage — same idea as the BasePage/BaseTest class you'd have had wrapping
WebDriver calls in Selenium, except Playwright's auto-wait means we don't
need explicit WebDriverWait/ExpectedConditions plumbing; locators auto-retry
until actionable or timeout.
"""
from playwright.sync_api import Page
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def goto(self, url: str):
        logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def click(self, selector: str):
        logger.info(f"Clicking: {selector}")
        self.page.locator(selector).click()

    def fill(self, selector: str, text: str):
        logger.info(f"Filling '{selector}' with '{text}'")
        self.page.locator(selector).fill(text)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def select_option(self, selector: str, value: str):
        self.page.locator(selector).select_option(value)

    def wait_for_url_contains(self, fragment: str, timeout: int = 5000):
        self.page.wait_for_url(f"**/*{fragment}*", timeout=timeout)
