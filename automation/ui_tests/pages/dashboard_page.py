class DashboardPage:
    def __init__(self, page):
        self.page = page

    def heading(self):
        return self.page.locator("h1")

    def device_cards(self):
        return self.page.locator("[data-testid^='device-card-']")

    def set_ac_temperature(self, device_id, temperature):
        self.page.fill(f"#tempInput-{device_id}", str(temperature))
        self.page.click("text=Set Temp")

    def set_tv_volume(self, device_id, volume):
        self.page.fill(f"#volumeInput-{device_id}", str(volume))
        self.page.click("text=Set Volume")

    def success_message(self):
        return self.page.locator("#message")

    def error_message(self):
        return self.page.locator("#errorMsg")

    def logout(self):
        self.page.click("text=Logout")