from django.test import TestCase, LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Create your tests here.
from users.models import User


# django の他のテストと同様、データベースはサンドボックスを作るため、
# ユーザーから作ってやる必要がある。
def create_logged_in_user(
        username="testuser",
        password="password",
        employee_code="9999999",
        email="testuser@example.com"
):
    user = User.objects.create_user(
        employee_code=employee_code,
        email=email,
        username=username,
        password=password,
    )
    user.save()


class MySeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):
        create_logged_in_user()

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys("9999999")
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys("password")

        self.selenium.find_element_by_id('Login').click()

        self.assertIn("Home | Profile Sheet", self.selenium.title)

