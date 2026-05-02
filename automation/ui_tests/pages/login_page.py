from pathlib import Path


class LoginPage:
    def __init__(self, page):
        self.page = page
        project_root = Path(__file__).resolve().parents[3]
        self.login_url = f"file://{project_root}/frontend/login.html"

    def open(self):
        self.page.goto(self.login_url)

    def login(self, email, password):
        self.page.fill("#email", email)
        self.page.fill("#password", password)
        self.page.click("#loginBtn")

    def get_error_message(self):
        return self.page.locator("#errorMsg")