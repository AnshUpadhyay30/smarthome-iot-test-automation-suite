import pytest
from playwright.sync_api import expect
from ui_tests.pages.login_page import LoginPage
from ui_tests.pages.dashboard_page import DashboardPage


def login_to_dashboard(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("admin@test.com", "admin123")
    page.wait_for_url("**/dashboard.html")
    expect(page.locator("h1")).to_have_text("SmartHome Dashboard")


@pytest.mark.ui
def test_dashboard_shows_four_devices(page):
    login_to_dashboard(page)

    dashboard = DashboardPage(page)

    expect(dashboard.heading()).to_have_text("SmartHome Dashboard")
    expect(dashboard.device_cards()).to_have_count(4)


@pytest.mark.ui
def test_update_ac_temperature_from_ui(page):
    login_to_dashboard(page)

    dashboard = DashboardPage(page)
    dashboard.set_ac_temperature(1, 24)

    expect(dashboard.success_message()).to_have_text("Temperature updated successfully")
    expect(page.locator("#temp-1")).to_have_text("24")


@pytest.mark.ui
@pytest.mark.negative
def test_invalid_ac_temperature_shows_error(page):
    login_to_dashboard(page)

    dashboard = DashboardPage(page)
    dashboard.set_ac_temperature(1, 31)

    expect(dashboard.error_message()).to_have_text("AC temperature must be between 16 and 30")


@pytest.mark.ui
def test_update_tv_volume_from_ui(page):
    login_to_dashboard(page)

    dashboard = DashboardPage(page)
    dashboard.set_tv_volume(2, 80)

    expect(dashboard.success_message()).to_have_text("Volume updated successfully")
    expect(page.locator("#volume-2")).to_have_text("80")


@pytest.mark.ui
def test_logout_redirects_to_login(page):
    login_to_dashboard(page)

    dashboard = DashboardPage(page)
    dashboard.logout()

    page.wait_for_url("**/login.html")
    expect(page.locator("h2")).to_have_text("SmartHome IoT")