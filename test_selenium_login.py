import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        # Open the login page
        self.driver.get('http://localhost:8000/login_page.html')

        # Wait for the page to load
        time.sleep(2)

        # Fill in the login form
        email_input = self.driver.find_element(By.ID, 'email')
        password_input = self.driver.find_element(By.ID, 'password')

        email_input.send_keys('test@example.com')
        password_input.send_keys('test_password')

        # Click the "Login" button
        login_button = self.driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
        login_button.click()

        # Wait for the login process to complete (add additional waits as needed)
        time.sleep(5)

        # Add assertions or further test steps based on the behavior you want to test

if __name__ == '__main__':
    unittest.main()
