import pytest
from selene import browser
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from utils import attach
from dotenv import load_dotenv
import os


@pytest.fixture(scope='function', autouse=True)
def browser_configuration():
    options = Options()
    selenoid_capabilities = {
        'browserName': 'chrome',
        'browserVersion': '126.0',
        'selenoid:options': {
            'enableVNC': True,
            'enableVideo': True
        }
    }
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f'https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub',
        options=options)

    browser.config.driver = driver
    browser.config.base_url = 'https://demoqa.com'

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
