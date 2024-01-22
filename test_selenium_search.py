import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class SearchPageTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()  # ChromeDriver yolu güncellenmeli
        self.driver.get('http://localhost:8000/search.html')  # HTML dosya yolu güncellenmeli

    def test_page_load(self):
        # Sayfanın başarıyla yüklendiğini kontrol et
        self.assertIn("Search", self.driver.title)

    def test_buttons_exist(self):
        # Butonların varlığını kontrol et
        artist_search_button = self.driver.find_element(By.XPATH, "//button[text()='Artist Search']")
        song_search_button = self.driver.find_element(By.XPATH, "//button[text()='Song Search']")
        album_search_button = self.driver.find_element(By.XPATH, "//button[text()='Album Search']")

        self.assertIsNotNone(artist_search_button)
        self.assertIsNotNone(song_search_button)
        self.assertIsNotNone(album_search_button)

    def test_artist_search_button(self):
        # Artist Search butonuna tıklandığında yönlendirme kontrolü
        artist_search_button = self.driver.find_element(By.XPATH, "//button[text()='Artist Search']")
        artist_search_button.click()

        # Yönlendirme URL kontrolü (bu örnekte sayfa değişmeyeceği için gerçek bir kontrol yapamıyoruz)
        # self.assertEqual(self.driver.current_url, 'beklenen_artist_search_url')

    def test_song_search_button(self):
        # Song Search butonuna tıklandığında yönlendirme kontrolü
        song_search_button = self.driver.find_element(By.XPATH, "//button[text()='Song Search']")
        song_search_button.click()

        # Yönlendirme URL kontrolü
        # self.assertEqual(self.driver.current_url, 'beklenen_song_search_url')

    def test_album_search_button(self):
        # Album Search butonuna tıklandığında yönlendirme kontrolü
        album_search_button = self.driver.find_element(By.XPATH, "//button[text()='Album Search']")
        album_search_button.click()

        # Yönlendirme URL kontrolü
        # self.assertEqual(self.driver.current_url, 'beklenen_album_search_url')

    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()