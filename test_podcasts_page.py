import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class PodcastsPageTest(unittest.TestCase):
    def setUp(self):
        # Set up the WebDriver
        self.driver = webdriver.Safari()
        self.driver.get("http://localhost:8000/podcasts.html") # Adjust the port if your app is running on a different one

   

    def test_podcast_list_population(self):
        time.sleep(2)
        driver = self.driver

        # Wait for at least one list item to be present in the podcast list
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#podcast-list li"))
        )

        # Now check if the podcast list has been populated
        podcast_list = driver.find_element(By.ID, "podcast-list")
        podcasts = podcast_list.find_elements(By.TAG_NAME, "li")
        self.assertTrue(len(podcasts) > 0, "The podcast list should be populated.")




    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
