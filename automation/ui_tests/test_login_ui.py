import pytest
from playwright.sync_api import expect
from ui_tests.pages.login_page import LoginPage


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_redirects_to_dashboard(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("admin@test.com", "admin123")

    page.wait_for_url("**/dashboard.html")

    expect(page.locator("h1")).to_have_text("SmartHome Dashboard")


@pytest.mark.ui
@pytest.mark.negative
def test_invalid_login_shows_error_message(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("admin@test.com", "wrongpass")

    expect(login_page.get_error_message()).to_have_text("Invalid email or password")