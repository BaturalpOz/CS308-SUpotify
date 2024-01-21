import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class TestSignUpAndLoginPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_forum_page(self):
        # Open the forum page
        self.driver.get('http://localhost:8000/forum.html')

        # Wait for the page to load
        time.sleep(2)

        # Interact with the comment section (add more actions based on your forum page behavior)
        comment_textarea = self.driver.find_element(By.ID, 'comment-textarea')
        comment_textarea.send_keys('This is a test comment.')

        post_comment_button = self.driver.find_element(By.CSS_SELECTOR, 'button.comment-btn')
        post_comment_button.click()

        # Wait for the comment to be posted
        time.sleep(5)

        # Verify the posted comment (you may need to enhance this verification based on your actual scenario)
        comments_container = self.driver.find_element(By.ID, 'comments-container')
        posted_comment = comments_container.find_element(By.XPATH, '//div[@class="comment"]/p[text()="This is a test comment."]')
        self.assertIsNotNone(posted_comment, 'Failed to post comment.')

if __name__ == '__main__':
    unittest.main()
