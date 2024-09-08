import pytest
from selene import browser, Config
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from utils import attach


@pytest.fixture(scope='function', autouse=True)
def browser_configuration():
    options = Options()
    selenoid_capabilities = {
        'browserName': 'chrome',
        'browserVersion': '126.0',
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': False
        }
    }

    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f'https://user1:1234@selenoid.autotests.cloud/wd/hub',
        options=options)

    browser.config.driver = driver
    browser.config.base_url = 'https://demoqa.com'

    yield browser

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
