import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PlaylistsPageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Safari()
        self.driver.get("http://127.0.0.1:8000/playlists.html")

        # Çerezi ekle
        self.driver.add_cookie({
            "name": "access_token_cookie",
            "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZnQ3WmtycUVDMzc5b1ZiMENhWTYiLCJleHAiOjE3MDU5MjI3MTV9.UUUheOREx3AYvuSxc6ZoIt6Byx_AV0Kpl_VuoHcQNpM",
            "path": "/"
        })
        
        # Çerez eklendikten sonra sayfayı yenileyin
        self.driver.refresh()

    def test_playlist_list_population(self):
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#playlist-list li"))
        )

        playlist_list = self.driver.find_element(By.ID, "playlist-list")
        playlists = playlist_list.find_elements(By.TAG_NAME, "li")
        self.assertTrue(len(playlists) > 0, "The playlist list should be populated.")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
