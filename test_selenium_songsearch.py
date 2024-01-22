import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



class ArtistSearchTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # ChromeDriver yolu güncellenmeli
        self.driver.get('http://localhost:8000/songsearch.html')  # HTML dosya yolu güncellenmeli

    def test_page_load(self):
        self.assertIn("Song Search", self.driver.title)

    def test_search_elements_exist(self):
        # Arama kutusu ve butonunun varlığını kontrol et
        search_box = self.driver.find_element(By.ID, "searchQuery")
        search_button = self.driver.find_element(By.XPATH, "//button[text()='Search']")

        self.assertIsNotNone(search_box)
        self.assertIsNotNone(search_button)

    def test_artist_search_functionality(self):
        search_box = self.driver.find_element(By.ID, "searchQuery")
        search_button = self.driver.find_element(By.XPATH, "//button[text()='Search']")

        test_song_name = "HANIMEFENDİ"  # Gerçek bir sanatçı adıyla değiştirin
        search_box.send_keys(test_song_name)
        search_button.click()

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()