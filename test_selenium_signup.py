import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSignUpPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_sign_up(self):
        # Open the sign-up page
        self.driver.get('http://localhost:8000/signup_page.html')

        # Wait for the page to load
        time.sleep(2)

        # Fill in the sign-up form
        username_input = self.driver.find_element(By.ID, 'username')
        email_input = self.driver.find_element(By.ID, 'email')
        password_input = self.driver.find_element(By.ID, 'password')

        username_input.send_keys('test_user')
        email_input.send_keys('test@example.com')
        password_input.send_keys('test_password')

        # Click the "Sign Up" button
        sign_up_button = self.driver.find_element(By.CSS_SELECTOR, 'button.btn-primary')
        sign_up_button.click()

        # Wait for the sign-up process to complete (add additional waits as needed)
        time.sleep(5)

        # Add assertions or further test steps based on the behavior you want to test

if __name__ == '__main__':
    unittest.main()
