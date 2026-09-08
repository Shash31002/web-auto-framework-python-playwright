import pytest
from utils.config_reader import Config
from utils.logger import get_logger

logger = get_logger(__name__)


# Override pytest-playwright's default browser context args with our config
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "ignore_https_errors": True,
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "headless": Config.HEADLESS,
        "slow_mo": Config.SLOW_MO,
    }


# Auto-screenshot on test failure, saved underreports/screenshots
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page is not None:
            screenshot_path = f"reports/screenshots/{item.name}.png"
            try:
                page.screenshot(path=screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                logger.warning(f"Could not capture screenshot: {e}")


def pytest_configure(config):
    logger.info(f"Running against BASE_URL={Config.BASE_URL} | headless={Config.HEADLESS}")
